from django.db import models
from django.contrib.auth import get_user_model



User = get_user_model()


class Game(models.Model):
    class WinRule(models.TextChoices):
        HIGH = "HIGH", "HIGH"
        LOW = "LOW", "LOW"

    class Status(models.TextChoices):
        REQUESTED = "REQUESTED", "REQUESTED"
        RESPONDED = "RESPONDED", "RESPONDED"
        FINISHED = "FINISHED", "FINISHED"

    attacker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attacker_games", null=True, blank=True)
    defender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="defender_games", null=True, blank=True)
    

    attacker_card = models.IntegerField()
    defender_card = models.IntegerField()

    win_rule = models.CharField(max_length=10, choices=WinRule.choices)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.REQUESTED)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Game {self.id}: {self.attacker} vs {self.defender}"
