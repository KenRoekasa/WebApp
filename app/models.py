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

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Blog(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

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
