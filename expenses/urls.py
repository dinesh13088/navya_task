from django.urls import path
from .views import (
    ExpenseListView,
    ExpenseCreateView,
    ExpenseUpdateView,
    ExpenseDeleteView,
)

urlpatterns = [
    path("", ExpenseListView.as_view(), name="expense-list"),
    path("create/", ExpenseCreateView.as_view(), name="expense-create"),
    path("<int:pk>/edit/", ExpenseUpdateView.as_view(), name="expense-edit"),
    path("<int:pk>/delete/", ExpenseDeleteView.as_view(), name="expense-delete"),
]
