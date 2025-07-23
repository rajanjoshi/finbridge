
from django import forms
from .models import SavingsGoal, Contribution

class SavingsGoalForm(forms.ModelForm):
    class Meta:
        model = SavingsGoal
        fields = ['title', 'description', 'target_amount', 'saved_amount', 'deadline']

        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }

class ContributionForm(forms.ModelForm):
    class Meta:
        model = Contribution
        fields = ['amount', 'note', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
