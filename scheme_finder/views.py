from django.shortcuts import render
from django.core.exceptions import ValidationError
from .models import Scheme

def scheme_form(request):
    eligible = []
    error = None
    if request.method == 'POST':
        try:
            age = int(request.POST.get('age', 0))
            income = int(request.POST.get('income', 0))
            if age < 0 or income < 0:
                raise ValidationError("Invalid age or income.")
            schemes = Scheme.objects.all()
            for s in schemes:
                if age >= s.min_age and income <= s.max_income:
                    eligible.append(s.name)
        except (ValueError, ValidationError):
            error = "Please enter valid numeric values for age and income."
    return render(request, 'scheme_finder/form.html', {'eligible': eligible, 'error': error})
