from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm


class RegisterView(CreateView):
    """Simple self-service registration page for new users."""
    form_class = CustomUserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("expense-list")

    def form_valid(self, form):
        response = super().form_valid(form)
       
        login(self.request, self.object)
        messages.success(self.request, "Welcome! Your account was created successfully.")
        return response
