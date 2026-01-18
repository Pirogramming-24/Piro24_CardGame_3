from django.urls import path
from django.views.generic import RedirectView
from . import views


urlpatterns = [

    # api 주소
    path("api/account/me/", views.me, name="me"),
    path("api/account/me/profile/", views.my_profile, name="my_profile"),

    # templates 기반 주소
    path("set-nickname/", views.set_nickname, name="set_nickname"),

    # allauth 로그인으로 리다이렉트
    path("login/", RedirectView.as_view(url="/accounts/login/", permanent=False)),
    path("signup/", RedirectView.as_view(url="/accounts/signup/", permanent=False)),
    path("logout/", RedirectView.as_view(url="/accounts/logout/", permanent=False))
]
