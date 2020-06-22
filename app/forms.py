import datetime

from django import forms
from django.forms import TypedChoiceField, Select, DateTimeInput, DateTimeField

from .models import Blog, Education, TechSkills, WorkExperience

year_choices = [(r, r) for r in range(1984, datetime.date.today().year + 1000)]


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'text',)


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ('school', 'location', 'start_year', 'end_year', 'field_of_study', 'description',)
        widgets = {
            'start_year': Select(choices=year_choices),
            'end_year': Select(choices=year_choices),
        }


class TechSkillsForm(forms.ModelForm):
    class Meta:
        model = TechSkills
        fields = ('skill',)


class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = ('title', 'company', 'location', 'start_date', 'end_date', 'description')
        widgets = {
            'start_date': forms.DateInput(format='%Y-%m-%d',attrs={'type': 'date'}),
            'end_date': forms.DateInput(format='%Y-%m-%d',attrs={'type': 'date'}),
        }
