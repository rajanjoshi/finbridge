
from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.conf import settings

class SavingsGoal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    saved_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    deadline = models.DateField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def progress_percent(self):
        return round((self.saved_amount / self.target_amount) * 100, 2) if self.target_amount else 0

    def is_close_to_deadline(self):
        delta = self.deadline - date.today()
        return delta.days <= 30 and self.progress_percent() < 75

class Contribution(models.Model):
    goal = models.ForeignKey(SavingsGoal, on_delete=models.CASCADE, related_name='contributions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=date.today)
    note = models.CharField(max_length=200, blank=True)
