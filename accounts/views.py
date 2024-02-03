from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.views.generic import View, FormView
from .forms import LoginUserForm, RegisterUserForm
from .models import User
from django.urls import reverse_lazy


class LoginUser(View):
    """
    this is CBV login user
    """

    def get(self, request):
        form = LoginUserForm()
        return render(request, "accounts/login.html", {"form": form})

    def post(self, request):
        form = LoginUserForm(request.POST)
        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("Todo:Todolist")
            elif not User.objects.filter(email=email):
                form.add_error("email", "Email is not valid")
            elif not User.objects.filter(password=password):
                form.add_error("password", "Password is not valid")
        return render(request, "accounts/login.html", {"form": form})


def logout_user(request):
    """
    this is for logout user
    """
    logout(request)
    return redirect("accounts:login")


class RegisterUser(FormView):
    """
    this is for Register user
    """

    template_name = "accounts/Register.html"
    form_class = RegisterUserForm
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        password = self.request.POST["password"]
        user = form.save(commit=False)
        user.is_superuser = True
        user.is_staff = True
        user.set_password(password)
        user.save()
        return super().form_valid(form)
