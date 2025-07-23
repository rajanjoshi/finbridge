from django.shortcuts import redirect
from .models import UserProfile

class RequireUserProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.path.startswith('/users/profile'):
            try:
                profile = request.user.profile
                if not all([profile.age, profile.region, profile.language, profile.persona]):
                    return redirect('profile')
            except UserProfile.DoesNotExist:
                return redirect('profile')

        return self.get_response(request)
