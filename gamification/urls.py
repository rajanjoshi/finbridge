from django.urls import path
from . import views

urlpatterns = [
    path('', views.gamification_dashboard, name='gamification_dashboard'),
    path('quiz/', views.financial_quiz_view, name='financial_quiz_view'),
    path('submit/', views.submit_quiz_view, name='submit_quiz'),
    path('result/', views.quiz_result_view, name='quiz_result'),
    path('history/', views.quiz_history_view, name='quiz_history'),
]
