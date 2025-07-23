from django import forms

class QuestionForm(forms.Form):
    question = forms.CharField(label="Your Question",required=False, max_length=500, widget=forms.TextInput(attrs={
        'placeholder': 'Ask your financial question...'
    }))
    preferred_language = forms.ChoiceField(
        choices=[('en', 'English'), ('hi', 'Hindi'), ('mr', 'Marathi')],
        label="Language", required=True
    )
    region = forms.ChoiceField(
        choices=[('IN', 'India'), ('US', 'United States')],
        label="Region", required=True
    )
    persona = forms.ChoiceField(
        choices=[('genz', 'Gen Z'), ('elderly', 'Elderly'), ('minority', 'Minority Group')],
        label="Persona", required=True
    )
