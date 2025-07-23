
from django.urls import path
from . import views

app_name = 'savings'

urlpatterns = [
    path('', views.index, name='index'),
    path('contribute/<int:goal_id>/', views.contribute, name='contribute'),
    path('complete/<int:goal_id>/', views.mark_complete, name='complete'),
    path('export/', views.export_csv, name='export'),
]
