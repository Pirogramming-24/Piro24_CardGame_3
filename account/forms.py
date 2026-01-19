from allauth.socialaccount.forms import SignupForm
from django import forms
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


class SocialSignupForm(SignupForm):
    nickname = forms.CharField(max_length=30)

    def save(self, request):
        user = super().save(request)

        profile, _ = Profile.objects.get_or_create(user=user)
        profile.nickname = self.cleaned_data["nickname"]
        profile.save()

        return user
