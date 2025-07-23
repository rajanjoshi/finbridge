from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from .models import UserProfile
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.utils import translation
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Allow post without CSRF token for language switch (optional)
def set_language_and_update_profile(request):
    if request.method == "POST":
        lang = request.POST.get("language")
        if lang:
            # Normalize 'en-us' to 'en'
            if lang == "en-us":
                lang = "en"

            translation.activate(lang)
            request.session[translation.LANGUAGE_SESSION_KEY] = lang

            # Optionally update the user's preferred language in their profile
            if request.user.is_authenticated and hasattr(request.user, "profile"):
                request.user.profile.language = lang
                request.user.profile.save()
    return redirect(request.META.get("HTTP_REFERER", "/"))

def register_view(request):
    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect("chat_view")  # or homepage
    else:
        user_form = CustomUserCreationForm()
        profile_form = UserProfileForm()

    return render(request, "users/register.html", {
        "user_form": user_form,
        "profile_form": profile_form,
    })

@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")  # Named URL
    else:
        form = UserProfileForm(instance=profile)

    return render(request, "users/profile.html", {
        "form": form
    })
