from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import Ticket
from cinema_admin.models import CinemaUser


class SignUpForm(UserCreationForm):
    class Meta:
        model = CinemaUser
        fields = ("username", "first_name", "last_name", "email",
                  "password1", "password2")
        widgets = {
            "username": forms.TextInput(attrs={"class": "widget_input"}),
            "first_name": forms.TextInput(attrs={"class": "widget_input"}),
            "last_name": forms.TextInput(attrs={"class": "widget_input"}),
            "email": forms.TextInput(attrs={"class": "widget_input"}),
            "password1": forms.PasswordInput(attrs={"class": "widget_input"}),
            "password2": forms.TextInput(attrs={"class": "widget_input"}),
        }


class BuyTicketForm(forms.ModelForm):
    def __init__(self, showtime=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if showtime:
            self.showtime = showtime
            self.fields['quantity'].widget.attrs["min"] = 1
            self.fields['quantity'].widget.attrs["max"] = \
                self.showtime.screen_blue.capacity - self.showtime.attendance

    class Meta:
        model = Ticket
        fields = ("quantity",)
        labels = {"quantity": "Order quantity "}
        widgets = {
            "quantity": forms.NumberInput(attrs={"class": "widget_quantity"}),
        }
