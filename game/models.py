from django.db import models
from django.contrib.auth import get_user_model



User = get_user_model()


class Game(models.Model):
    class WinRule(models.TextChoices):
        HIGH = "HIGH", "HIGH"
        LOW = "LOW", "LOW"

    class Status(models.TextChoices):
        REQUESTED = "REQUESTED", "진행중"
        RESPONDED = "RESPONDED", "CounterAttack"
        FINISHED = "FINISHED", "종료"

    class Result(models.TextChoices):
        WIN = 'win', '승리'
        LOSE = 'lose', '패배'
        DRAW = 'draw', '무승부'
        PENDING = 'pending', '대기중'

    attacker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attacker_games", null=True, blank=True)
    defender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="defender_games", null=True, blank=True)
    

    attacker_card = models.IntegerField()
    defender_card = models.IntegerField(null=True, blank=True)

    win_rule = models.CharField(max_length=10, choices=WinRule.choices)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.REQUESTED)

    attacker_result = models.CharField(max_length=10, choices=Result.choices, default=Result.PENDING)
    defender_result = models.CharField(max_length=10, choices=Result.choices, default=Result.PENDING)

    attacker_score_change = models.IntegerField(default=0)
    defender_score_change = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Game {self.id}: {self.attacker} vs {self.defender}"

    def display_status_for(self, user):
        if self.status == self.Status.REQUESTED:
            if self.defender == user:
                return "CounterAttack"
            return "진행중"

        if self.status == self.Status.FINISHED:
            return "종료"

        return ""

    def can_cancel(self, user):
        return (
            self.status == self.Status.REQUESTED
            and self.attacker == user
        )

    def can_counter(self, user):
        return (
            self.status == self.Status.REQUESTED
            and self.defender == user
        )

    def result_for(self, user):
        if user == self.attacker:
            return self.get_attacker_result_display()
        elif user == self.defender:
            return self.get_defender_result_display()
        return ''

    def score_for(self, user):
        if user == self.attacker:
            return self.attacker_score_change
        elif user == self.defender:
            return self.defender_score_change
        return 0

    class Meta:
        ordering = ['-created_at']
        verbose_name = '게임'
        verbose_name_plural = '게임 목록'

