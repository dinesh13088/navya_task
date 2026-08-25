# Expense Tracker

A simple Django web app for tracking personal expenses. Authenticated users
can create, view, update, and delete their own expenses.

## Features

- Custom user model (`accounts.CustomUser`) with Django's built-in auth
- Login / logout / registration
- Expense list, create, update, delete (class-based views)
- Users can only ever see or modify their own expenses
- Server-side validation: title required, amount must be > 0
- Success/error messages via Django's messages framework
- "Total this month" and "filtered total" summary cards on the list page
-  Filter by category and date range


## Project layout

```
expense_tracker/       # project settings, root urls
accounts/               # custom user model, registration view
expenses/                # Expense model, views, forms
templates/               # base.html, registration/, expenses/
static/css/style.css     # css
```

## Setup

```bash
# from the project root (this folder)
uv venv
source venv/bin/activate     
 # Windows: venv\Scripts\activate

uv pip install django

python manage.py migrate
python manage.py runserver

#to create the superuser with username and password

python manage.py createsuperuser  

```

Visit **http://127.0.0.1:8000/** — you'll be redirected to log in.

## Testing the app manually

1. **Register**: go to `/accounts/register/` and create an account (you're
   logged in automatically afterward).
2. **Add an expense**: click "Add Expense", fill in title/amount/category/date,
   submit. You'll see a "Expense added successfully" message and it appears
   in the table.
3. **Validation**: try submitting a blank title or a negative/zero amount —
   the form re-renders with an inline error and nothing is saved.
4. **Filter**: use the category dropdown or date range fields at the top of
   the list and click "Filter" (this updates the URL query string, e.g.
   `/expenses/?category=Food&start_date=2026-08-01`).
5. **Edit**: click "Edit" on a row, change a value, save.
6. **Delete**: click "Delete", confirm on the confirmation page.
7. **Ownership**: register a second account-
   it will see an empty expense list, and cannot reach the first user's
   `/expenses/<id>/edit/` or `/expenses/<id>/delete/` URLs 
8. **Logout**: click "Logout" in the top bar — you'll be redirected to the
   login page, and `/expenses/` becomes inaccessible until you log back in.



```bash
```

## Approach

- **Custom user model**: `accounts.CustomUser` subclasses `AbstractUser`
  and is set as `AUTH_USER_MODEL` from the start
  
- **Views**: All expense views are class-based (`ListView`, `CreateView`,
  `UpdateView`, `DeleteView`). A small `UserOwnsExpenseMixin` combines
  `LoginRequiredMixin` with a `get_queryset()` override that filters to
  `request.user`'s expenses — this is what makes edit/delete on someone
  else's expense return a 404 instead of leaking data, and it's shared
  across the list/edit/delete views to avoid repeating the same filter.
- **Ownership on create**: `ExpenseCreateView.form_valid()` sets
  `form.instance.user = request.user` before saving, so the user field is
  never exposed in the form itself.
- **Validation**: enforced both at the model level (`MinValueValidator` on
  `amount`) and the form level (`ExpenseForm.clean_title` /
  `clean_amount`), so invalid data can't reach the database via the form
  and errors render inline next to the field.
- **Filtering**: implemented by overriding `ExpenseListView.get_queryset()`
  to read `category`, `start_date`, `end_date` from `request.GET`; the
  filter form re-submits as a GET request so results are shareable/
  bookmarkable URLs.
- **Templates**: a single `base.html` with a top nav and messages block,
  extended by each page. Forms are rendered field-by-field (not
  `{{ form }}` as-is) so labels and errors can be styled consistently.
- **Static files**: one small `style.css`, no CSS framework or build step,
  kept intentionally simple per the brief.





## Admin

A Django admin site is available at `/admin/` (after `createsuperuser`) for
inspecting users and expenses directly.
