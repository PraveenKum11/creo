from django.urls import path

from cauth import views

# Give namespace to the app
# so that login view can be called within
# navbar using app_name:view_name
app_name = "cauth"

urlpatterns = [
    path("login/", views.login_user, name = "login"),
    path("logout/", views.logout_user, name = "logout"),
    path("register/", views.register, name = "register"),
]

htmx_urlpatterns = [
    path("check_username/", views.check_username, name = "check_username"),
]

urlpatterns += htmx_urlpatterns