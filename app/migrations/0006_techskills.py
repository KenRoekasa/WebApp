# Generated by Django 2.2.12 on 2020-06-12 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20200609_1710'),
    ]

    operations = [
        migrations.CreateModel(
            name='TechSkills',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.CharField(max_length=255)),
            ],
        ),
    ]
