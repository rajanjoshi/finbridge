from django.shortcuts import render
from .models import Lesson

def index(request):
    topics = Lesson.objects.all()
    return render(request, 'learn_finance/index.html', {'topics': ['Finance']})
