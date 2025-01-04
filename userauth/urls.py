from django.urls import path
from userauth import views

app_name = "userauth"

urlpatterns = [
    path("sign-up/", views.register_view, name="sign-up"),
    path("login/", views.login_view, name="login"),
    path("login/<str:next>/", views.login_view, name="login-next"),
    path("logout/", views.logout_view, name="logout"),
    path("my-account/", views.user_profile, name="my-account"),
    path("edit-info/", views.edit_profile, name="edit-info"),
    path("change-password/", views.change_password, name='change-password')
]