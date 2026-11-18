from django.contrib import admin
from django.contrib.auth import views
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", views.LoginView.as_view(template_name="onlinecourse/login.html"), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("", include("onlinecourse.urls")),
]
