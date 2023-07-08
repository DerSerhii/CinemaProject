from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q, ProtectedError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.utils import timezone as tz

from cinema.models import Showtime, ScreenCinema, Film
from staff.forms import ScreenForm, ShowtimeForm, ShowtimeEditForm
from utils import select_show


class FilmView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "staff/film.html"
    context_object_name = "films"
    queryset = Film.objects.all()
    paginate_by = 3

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = "Films for rental"
        context['films_count'] = self.queryset.count()
        return context


class CreateFilmView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Film
    fields = "__all__"
    template_name = "staff/create-film.html"
    success_url = reverse_lazy("film")
    login_url = reverse_lazy("sign-in")

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = "Create film"
        return context


class EditFilmView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    pk_url_kwarg = "film_id"
    template_name = "staff/edit-film.html"
    model = Film
    fields = "__all__"
    success_url = reverse_lazy("film")
    login_url = reverse_lazy("sign-in")

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        film_id = self.kwargs["film_id"]

        context["title"] = "Edit Film"
        context["film_id"] = film_id
        return context


class RemoveFilmView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    pk_url_kwarg = "film_id"
    model = Film
    success_url = reverse_lazy("film")
    login_url = reverse_lazy("sign-in")

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        success_url = self.get_success_url()

        try:
            success_message = "The film %s removed" % self.object.name
            self.object.delete()
            messages.success(self.request, success_message)
            return HttpResponseRedirect(success_url)
        except ProtectedError:
            error_message = \
                    "The film <%s> can't be deleted because it's in rental" \
                    % self.object.name
            messages.error(self.request, error_message)
            return HttpResponseRedirect(
                reverse("edit-film", kwargs={"film_id": self.kwargs["film_id"]}))


class ScreenShowtimeAllView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'staff/screen-all.html'
    model = Showtime
    context_object_name = 'showtimes'
    login_url = reverse_lazy("sign-in")

    def test_func(self):
        return self.request.user.is_superuser


class CreateScreenView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = ScreenForm
    template_name = "staff/create-screen.html"
    success_url = reverse_lazy("screen-showtime", kwargs={"scr_id": 0})
    login_url = reverse_lazy("sign-in")

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = "Create screen"
        return context


class EditScreenView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    pk_url_kwarg = "scr_id"
    template_name = "staff/edit-screen.html"
    model = ScreenCinema
    fields = "__all__"
    success_url = reverse_lazy("screen-showtime", kwargs={"scr_id": 0})
    login_url = reverse_lazy("sign-in")

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        screen_id = self.kwargs["scr_id"]

        context["title"] = "Edit Screen"
        context["scr_id"] = screen_id
        context['screen'] = Showtime.objects.filter(screen=screen_id).count()
        return context


class RemoveScreenView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    pk_url_kwarg = "scr_id"
    model = ScreenCinema
    success_url = reverse_lazy("screen-showtime", kwargs={"scr_id": 0})
    login_url = reverse_lazy("sign-in")

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        success_url = self.get_success_url()

        try:
            success_message = "The screen %s removed" % self.object.name
            self.object.delete()
            messages.success(self.request, success_message)
            return HttpResponseRedirect(success_url)
        except ProtectedError:
            error_message = \
                "The screen %s can be deleted when all showtime in it end" \
                % self.object.name
            messages.error(self.request, error_message)
            return HttpResponseRedirect(
                reverse("edit-screen", kwargs={"scr_id": self.kwargs["scr_id"]}))


class ScreenShowtimeView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'staff/admin-home.html'
    context_object_name = 'showtime'
    login_url = reverse_lazy("sign-in")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.select_day = None
        self.screen_id = None

    def test_func(self):
        return self.request.user.is_superuser

    def get_queryset(self):
        query_date_str = self.request.GET.get("day")
        self.select_day = select_show.get_selected_day(query_date_str)
        self.screen_id = self.kwargs["scr_id"]

        screen_filter = Q(screen=self.screen_id)
        day_filter = Q(start__date=self.select_day)
        sw_filter = screen_filter & day_filter if self.screen_id else day_filter

        return Showtime.objects.filter(sw_filter).order_by('start').\
            exclude(start__lte=tz.localtime(tz.now()))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # filter settings
        filter_date = Q(showtime__start__date=self.select_day)
        filter_time_start = Q(showtime__start__gte=tz.localtime(tz.now()))
        filter_date_all = Q(start__date=self.select_day)
        filter_time_start_all = Q(start__gte=tz.localtime(tz.now()))

        if self.select_day.date() == tz.localtime(tz.now()).date():
            showtime = Count('showtime', filter=filter_date & filter_time_start)
            showtime_all = filter_date_all & filter_time_start_all
        else:
            showtime = Count('showtime', filter=filter_date)
            showtime_all = filter_date_all

        context['day_selected'] = self.select_day
        context['screen_selected'] = self.screen_id
        context['screens'] = ScreenCinema.objects.annotate(count=showtime)
        context['screens_all'] = Showtime.objects.filter(showtime_all).count()

        return context


class CreateShowtimeView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = ShowtimeForm
    template_name = "staff/create-showtime.html"
    success_url = reverse_lazy("screen-showtime", kwargs={"scr_id": 0})
    login_url = reverse_lazy("sign-in")

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create showtime"
        return context


class EditShowtimeView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    pk_url_kwarg = "show_id"
    template_name = "staff/edit-showtime.html"
    model = Showtime
    form_class = ShowtimeEditForm
    success_url = reverse_lazy("screen-showtime", kwargs={"scr_id": 0})
    login_url = reverse_lazy("sign-in")

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        screen_id = self.kwargs["show_id"]

        context["title"] = "Edit Showtime"
        context["show_id"] = screen_id
        context["attendance"] = self.object.attendance
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        showtime_id = self.kwargs[self.pk_url_kwarg]
        attendance = self.object.attendance

        kwargs["showtime_id"] = showtime_id
        kwargs["attendance"] = attendance
        return kwargs


class RemoveShowtimeView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    pk_url_kwarg = "show_id"
    model = Showtime
    success_url = reverse_lazy("screen-showtime", kwargs={"scr_id": 0})
    login_url = reverse_lazy("sign-in")

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        success_url = self.get_success_url()

        if self.object.date < tz.localtime(tz.now()).date():
            Showtime.objects.get(pk=self.kwargs["show_id"]).tickets.all().delete()
        
        try:
            success_message = "The showtime %s removed" % self.object
            self.object.delete()
            messages.success(self.request, success_message)
            return HttpResponseRedirect(success_url)
        except ProtectedError:
            error_message = \
                "The showtime %s with sold tickets cannot be deleted" \
                % self.object
            messages.error(self.request, error_message)
            return HttpResponseRedirect(
                reverse("edit-showtime", kwargs={"show_id": self.kwargs["show_id"]}))
