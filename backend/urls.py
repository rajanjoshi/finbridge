from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.i18n import i18n_patterns
from ai_assistant.views import set_language_and_update_profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('ai_assistant.urls')),
    path('gamification/', include('gamification.urls')),
    path('savings/', include('savings.urls', namespace='savings')),
    #path('schemes/', include('scheme_finder.urls')),
    #path('learn/', include('learn_finance.urls')),
    path("users/", include("users.urls")),
    path("rag_admin/", include("rag_admin.urls")),
    path("users/", include("users.urls")),
    path('about/', include('about.urls')),
    path('i18n/setlang/', set_language_and_update_profile, name='set_language')
]
