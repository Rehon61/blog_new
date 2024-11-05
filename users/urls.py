# users/urls.py
# С префиксом в маршруте /users/
from django.urls import path
from . import views
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Маршруты связанные с восстановлением паролей
    # Маршрут для сброса пароля
    path("password-reset/", auth_views.PasswordResetView.as_view(
        template_name="users/password_reset_form.html",
        email_template_name="users/password_reset_email.html",
        success_url=reverse_lazy("password_reset_done"),
    ), name="password_reset",
         ),

    # Маршрут для подтверждения сброса пароля
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="users/password_reset_done.html"
    ), name="password_reset_done",
         ),

    # Маршрут для ввода нового пароля
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="users/password_reset_confirm.html",
        success_url=reverse_lazy("password_reset_complete"),
    ), name="password_reset_confirm",
         ),

    # Маршрут для завершения сброса пароля
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
        template_name="users/password_reset_complete.html"
    ), name="password_reset_complete",
         ),
]