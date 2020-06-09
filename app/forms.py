from django import forms
from .models import Blog,Education


class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ('title', 'text',)


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields =('school','start_year','end_year','field_of_study','description',)