from django import forms

class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions', [])
        super().__init__(*args, **kwargs)
        for i, q in enumerate(questions):
            self.fields[f"answer_{i}"] = forms.ChoiceField(
                label=q["question"],
                choices=[(opt, opt) for opt in q["options"]],
                widget=forms.RadioSelect,
                required=True
            )
