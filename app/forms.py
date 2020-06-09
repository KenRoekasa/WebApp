import datetime

from django import forms
from .models import Blog, Education


def year_choices():
    return [(r, r) for r in range(1984, datetime.date.today().year + 1)]


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'text',)


class EducationForm(forms.ModelForm):
    start_year = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=datetime.date.today().year)
    end_year = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=datetime.date.today().year)
    class Meta:
        model = Education
        fields = ('school', 'location', 'field_of_study', 'description',)
