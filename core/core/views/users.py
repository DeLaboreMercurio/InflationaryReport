from unittest.mock import DEFAULT
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _

from core.forms.registration import NewUserForm, BalanceForm


def register_request(request):
    if request.method == "POST":
        user_form = NewUserForm(request.POST)
        balance_form = BalanceForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(request, user)
            messages.success(request, _("Registration successful."))
            if balance_form.is_valid():
                balance_form.save()
            return redirect("home")
        messages.warning(request, _("Unsuccessful registration. Invalid information."))

    user_form = NewUserForm()
    balance_form = BalanceForm(initial={"balance": 0})
    return render(
        request=request,
        template_name="registration/register.html",
        context={"register_form": user_form, "balance_form": balance_form},
    )


def login_request(request):
    if request.method == "POST":
        if "login" in request.POST:
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.info(request, f"You are now logged in as {username}.")
                    return redirect("home")
                else:
                    messages.warning(request, _("Invalid username or password."))
            else:
                messages.warning(request, _("Invalid username or password."))

        if "register" in request.POST:
            user_form = NewUserForm(request.POST)
            balance_form = BalanceForm(request.POST)
            if user_form.is_valid():
                user = user_form.save()
                login(request, user)
                messages.success(request, _("Registration successful."))
                if balance_form.is_valid():
                    balance_form.save()
                return redirect("home")
            messages.warning(request, _("Unsuccessful registration. Invalid information."))

    login_form = AuthenticationForm()
    register_form = NewUserForm()
    balance_form = BalanceForm(initial={"balance": 0})
    return render(
        request=request,
        template_name="registration/login.html",
        context={
            "login_form": login_form,
            "register_form": register_form,
            "balance_form": balance_form,
        },
    )


def logout_request(request):
    logout(request)
    return redirect("login")
