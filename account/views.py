from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy


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
    p = getattr(request.user, "profile", None)
    if not p:
        return Response({"detail": "profile missing"}, status=500)
    context = {
        "score": p.score,
        "nickname" : p.nickname,
    }
    return Response(context)

def set_nickname(request):
    None