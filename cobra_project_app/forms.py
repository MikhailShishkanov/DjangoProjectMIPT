from django import forms
from cobra_project_app.models import Test, Question, Answer

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True})
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True})
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['name', 'correctness']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'correctness': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }