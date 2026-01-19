from django.shortcuts import render, redirect

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import Profile


# Create your views here.

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    u = request.user
    return Response({
        "id": u.id,
        "username": u.username,
        "email": u.email,
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    return Response({
        "score": profile.score,
        "nickname": profile.nickname,
    })

@login_required
def set_nickname(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        nickname = request.POST.get("nickname")
        if nickname:
            profile.nickname = nickname
            profile.save()
            return redirect("/")  # 게임 메인 등

    return render(request, "account/set_nickname.html")
    



def main(request):
    return render(request, "account/main.html")
