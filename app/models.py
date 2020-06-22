import datetime

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone


def year_choices():
    return [(r, r) for r in range(1984, datetime.date.today().year + 5)]


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.TextField()
    image = models.ImageField(upload_to='images')
    published_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title


class Blog(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title


class Education(models.Model):
    school = models.CharField(max_length=255)
    location = models.CharField(max_length=64)
    description = models.TextField()
    start_year = models.PositiveIntegerField(default=timezone.now().year,
                                             validators=[MinValueValidator(1984), MaxValueValidator(3000)])
    end_year = models.PositiveIntegerField(default=timezone.now().year,
                                           validators=[MinValueValidator(1984), MaxValueValidator(3000)])
    field_of_study = models.CharField(max_length=255)

    def __str__(self):
        return self.school


class TechSkills(models.Model):
    skill = models.CharField(max_length=255)

    def __str__(self):
        return self.school


class WorkExperience(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)

    def start_date_mY(self):
        return self.start_date.strftime('%B %Y')

    def end_date_mY(self):
        return self.end_date.strftime('%B %Y')
