from allauth.socialaccount.forms import SignupForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

class SocialSignupForm(SignupForm):
    nickname = forms.CharField(max_length=30)

    def save(self, request):
        user = super().save(request)
        user.profile.nickname = self.cleaned_data["nickname"]
        user.profile.save()
        return user

