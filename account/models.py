from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    score = models.IntegerField(default=0)

    # 추가로 필요한 정보들 여기에 계속 추가
    nickname = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"
