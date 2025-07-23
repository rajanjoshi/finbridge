from django.urls import path
from .views import index

app_name = 'learn_finance'
urlpatterns = [ path('', index, name='index') ]
