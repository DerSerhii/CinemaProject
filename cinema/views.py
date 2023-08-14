from datetime import datetime

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import Q, Sum, F
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, ListView
from django.utils import timezone as tz

from cinema.forms import SignUpForm, BuyTicketForm
from cinema.models import Showtime, Film, Spectator, Ticket


class CinemaHomePageView(TemplateView):
    """
    This object represents the first view that a visitor sees when visiting the site.
    """
    template_name = "cinema/cinema-home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get the utils day from template
        select_day = self.get_selected_day()

        # add new context
        context["day_selected"] = select_day
        context["showtime"] = self.get_films_with_showtimes_on_this_day(select_day)

        return context

    def get_selected_day(self):
        """
        Returns the day selected by the user from the template.
        if the choice has not yet been made, it returns the current date by default.
        """
        if day := self.request.GET.get('day'):
            return tz.datetime.strptime(day, "%m/%d/%Y").date()
        return tz.localdate()

    @staticmethod
    def get_films_with_showtimes_on_this_day(select_day):
        """
        Returns a list of Films with QuerySets of Showtimes on this day
        """

        # get films on this day
        query_film_on_this_day = \
            Showtime.objects.values("film").filter(start=select_day).distinct()

        list_film_id_on_this_day = [i.get("film") for i in query_film_on_this_day]

        # get films with showtimes on this day
        films_with_showtime_on_this_day = []

        q_select_day = Q(start=select_day)
        q_time_start_gte_now = Q(time_start__gte=tz.localtime(tz.now()).time())

        if select_day == tz.localtime(tz.now()).date():
            q_filter = q_select_day & q_time_start_gte_now
        else:
            q_filter = q_select_day
    
        for film_id in list_film_id_on_this_day:
            film = Film.objects.get(id=film_id). \
                showtime_set.filter(q_filter).order_by("time_start")
            films_with_showtime_on_this_day.append(film)

        return films_with_showtime_on_this_day


class ShowtimeView(DetailView):
    pk_url_kwarg = "show_id"
    template_name = "cinema/showtime.html"
    model = Showtime
    context_object_name = "showtime"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["buy_form"] = BuyTicketForm(self.object, initial={"quantity": 1})
        context["free_seats"] = self.object.screen_blue.capacity - self.object.attendance
        return context


class SignUpView(CreateView):
    template_name = "cinema/sign-up.html"
    form_class = SignUpForm
    success_message = "Congrats, %(username)s! You have successfully registered"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        success_message = self.success_message % form.cleaned_data
        messages.success(self.request, success_message)
        return redirect("cinema-home")


class SignInView(SuccessMessageMixin, LoginView):
    template_name = "cinema/sign-in.html"
    form_class = AuthenticationForm
    success_message = "Hey, %(username)s! You have successfully logged in"

    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse("screen-showtime", kwargs={"scr_id": 0})
        return reverse("cinema-home")


class Logout(LogoutView):
    next_page = "cinema-home"


class ProfileSpectatorView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    pk_url_kwarg = "spec_id"
    template_name = "cinema/profile.html"
    model = Spectator
    fields = ("first_name", "last_name", "email")
    login_url = reverse_lazy("sign-in")
    success_message = "You have successfully modified your profile"


class WalletSpectatorView(LoginRequiredMixin, UpdateView):
    pk_url_kwarg = "spec_id"
    template_name = "cinema/wallet.html"
    model = Spectator
    fields = ("wallet", )
    login_url = reverse_lazy("sign-in")
    success_url = reverse_lazy("cinema-home")
    success_message = "You have successfully deposited ₴%(wallet)s"
    initial = {"wallet": 1000}

    def form_valid(self, form):
        wallet_form = form.save(commit=False)

        # add money to existing
        current_wallet = self.request.user.wallet
        wallet_form.wallet += current_wallet

        with transaction.atomic():
            wallet_form.save()

        # add message
        success_message = self.success_message % form.cleaned_data
        messages.success(self.request, success_message)

        return super().form_valid(form=form)

    # def get_initial(self):
    #     return {'wallet': 1000}


class BuyTicketView(LoginRequiredMixin, CreateView):
    form_class = BuyTicketForm
    pk_url_kwarg = "show_id"
    http_method_names = ["post"]
    success_url = reverse_lazy("cinema-home")
    login_url = reverse_lazy("sign-in")

    def form_valid(self, form):
        ticket = form.save(commit=False)

        ticket.spectator = self.request.user

        showtime_id = self.kwargs[self.pk_url_kwarg]
        ticket.showtime = Showtime.objects.get(id=showtime_id)

        # money sufficiency check
        wallet_spectator = ticket.spectator.wallet
        ticket_total_price = ticket.showtime.price * ticket.quantity
 
        if ticket_total_price > wallet_spectator:
            return redirect(
                reverse("wallet", kwargs={"spec_id": ticket.spectator.pk}))

        ticket.spectator.wallet -= ticket_total_price
        ticket.showtime.attendance += ticket.quantity

        with transaction.atomic():
            ticket.spectator.save()
            ticket.showtime.save()
            ticket.save()

        return super().form_valid(form=form)


class SpectatorPurchaseView(LoginRequiredMixin, ListView):
    template_name = "cinema/spectator-purchase.html"
    context_object_name = "purchases"
    login_url = reverse_lazy("sign-in")

    def get_queryset(self):
        return Ticket.objects.filter(spectator=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        visit = Ticket.objects.filter(spectator=self.request.user)

        context["visit"] = visit.count()
        context["ticket"] = visit.aggregate(s=Sum(F("quantity")))["s"]
        context["sum_money"] = visit.aggregate(s=Sum(F("showtime__price")*F("quantity")))["s"]
        return context
