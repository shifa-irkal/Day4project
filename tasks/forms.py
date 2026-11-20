from django import forms
from .models import Task

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'description', 'completed']

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter task title'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3
                }
            ),
            'completed': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if len(title) < 3:
            raise forms.ValidationError(
                'Task title must be at least 3 characters long.'
            )

        return title