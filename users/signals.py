from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import translation
from django.contrib.auth.signals import user_logged_in
from django.conf import settings
from users.models import UserProfile
LANGUAGE_SESSION_KEY = settings.LANGUAGE_COOKIE_NAME

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, "profile"):
        UserProfile.objects.create(user=instance)

@receiver(user_logged_in)
def set_language_on_login(sender, user, request, **kwargs):
    if hasattr(user, "profile") and user.profile.language:
        lang = user.profile.language
        translation.activate(lang)
        request.session[LANGUAGE_SESSION_KEY] = user.profile.language
