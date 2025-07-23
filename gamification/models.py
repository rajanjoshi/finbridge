from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class QuizQuestion(models.Model):
    question_text = models.TextField(_("Question"))
    correct_answer = models.TextField(_("Correct Answer"))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text[:100]


class UserQuizAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    user_answer = models.TextField(_("Your Answer"))
    is_correct = models.BooleanField(default=False)
    attempted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {'✅' if self.is_correct else '❌'}"

from django.db import models
from django.conf import settings

class QuizSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.FloatField()
    total_questions = models.PositiveIntegerField()
    correct_answers = models.PositiveIntegerField(null=True)
    badge = models.CharField(max_length=20, blank=True, null=True)
    taken_on = models.DateTimeField(auto_now_add=True)

    def percentage(self):
        if self.total_questions > 0:
            return round((self.score / self.total_questions) * 100, 2)
        return 0
        
    def __str__(self):
        return f"{self.user.username} - {self.score}% on {self.taken_on.strftime('%Y-%m-%d')}"


class Badge(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=100, default="🏅")

    def __str__(self):
        return f"{self.icon} {self.name}"


class UserBadge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    awarded_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} → {self.badge.name}"
