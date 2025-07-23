from django.urls import path
from .views import scheme_form

app_name = 'scheme_finder'
urlpatterns = [ path('', scheme_form, name='form') ]
