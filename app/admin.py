from django.contrib import admin
from .models import Project, Blog, Education, WorkExperience, TechSkills, AcademicProjects

# Register your models here.
admin.site.register(Project)
admin.site.register(Blog)
admin.site.register(Education)
admin.site.register(TechSkills)
admin.site.register(AcademicProjects)
admin.site.register(WorkExperience)
