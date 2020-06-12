import datetime

from django import forms
from django.forms import TypedChoiceField, Select

from .models import Blog, Education, TechSkills

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
