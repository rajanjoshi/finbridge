from django.urls import path
from . import views  # ✅ FIXED: Import views module

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path("set-language/", views.set_language_and_update_profile, name="set_language")
]