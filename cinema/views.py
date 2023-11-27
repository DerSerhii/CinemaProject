from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import F, Sum
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView, ListView


from cinema.forms import SignUpForm, BuyTicketForm
from cinema.models import Showtime, Ticket
from cinema_admin.models import SpectatorProfile
from utils import CinemaShowtimeMixin


class CinemaHomePageView(CinemaShowtimeMixin, ListView):
    """
    View for the cinema homepage, displaying a list of films along with their showtimes.
    """
    template_name = 'cinema/cinema-home.html'
    context_object_name = 'films'

    def get_context_data(self, **kwargs) -> dict:
        """
        Adds additional context data to the view's template:
        - `selected_day`.
        """
        context = super().get_context_data(**kwargs)
        additional_context = self.get_additional_context()
        context.update(additional_context)
        return context


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
            return reverse('admin-showtimes', kwargs={'screen_slug': 'all'})
        return reverse("cinema-home")


class Logout(LogoutView):
    next_page = "cinema-home"


class ProfileSpectatorView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    pk_url_kwarg = "spec_id"
    template_name = "cinema/profile.html"
    model = SpectatorProfile
    fields = ("first_name", "last_name", "email")
    login_url = reverse_lazy("sign-in")
    success_message = "You have successfully modified your profile"


class WalletSpectatorView(LoginRequiredMixin, UpdateView):
    pk_url_kwarg = "spec_id"
    template_name = "cinema/wallet.html"
    model = SpectatorProfile
    fields = ("wallet", )
    login_url = reverse_lazy("sign-in")
    success_url = reverse_lazy("cinema-home")
    success_message = "You have successfully deposited ₴%(wallet)s"
    initial = {"wallet": 1000}

    def form_valid(self, form):
        wallet_form = form.save(commit=False)

        # add money to existing
        current_wallet = self.request.superuser.wallet
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

        ticket.spectator = self.request.superuser

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
        return Ticket.objects.filter(spectator=self.request.superuser)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        visit = Ticket.objects.filter(spectator=self.request.superuser)

        context["visit"] = visit.count()
        context["ticket"] = visit.aggregate(s=Sum(F("quantity")))["s"]
        context["sum_money"] = visit.aggregate(s=Sum(F("showtime__price")*F("quantity")))["s"]
        return context
