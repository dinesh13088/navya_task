from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import ExpenseForm
from .models import Expense


class UserOwnsExpenseMixin(LoginRequiredMixin):
    
    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)


class ExpenseListView(UserOwnsExpenseMixin, ListView):
    """Shows all expenses for the logged-in user, with optional filters."""

    model = Expense
    template_name = "expenses/expense_list.html"
    context_object_name = "expenses"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()

        category = self.request.GET.get("category")
        if category:
            queryset = queryset.filter(category=category)

        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Expense.CATEGORY_CHOICES
        context["selected_category"] = self.request.GET.get("category", "")
        context["start_date"] = self.request.GET.get("start_date", "")
        context["end_date"] = self.request.GET.get("end_date", "")

    
        today = timezone.now().date()
        month_total = Expense.objects.filter(
            user=self.request.user,
            date__year=today.year,
            date__month=today.month,
        ).aggregate(total=Sum("amount"))["total"]
        context["month_total"] = month_total or 0


        filtered_total = self.get_queryset().aggregate(total=Sum("amount"))["total"]
        context["filtered_total"] = filtered_total or 0

        return context


class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = "expenses/expense_form.html"
    success_url = reverse_lazy("expense-list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Expense added successfully.")
        return super().form_valid(form)


class ExpenseUpdateView(UserOwnsExpenseMixin, UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = "expenses/expense_form.html"
    success_url = reverse_lazy("expense-list")

    def form_valid(self, form):
        messages.success(self.request, "Expense updated successfully.")
        return super().form_valid(form)


class ExpenseDeleteView(UserOwnsExpenseMixin, DeleteView):
    model = Expense
    template_name = "expenses/expense_confirm_delete.html"
    success_url = reverse_lazy("expense-list")

    def form_valid(self, form):
        messages.success(self.request, "Expense deleted successfully.")
        return super().form_valid(form)
