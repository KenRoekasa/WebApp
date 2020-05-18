from django.shortcuts import render
from .models import Project


# Create your views here.
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'app/portfolio_list.html', {'projects': projects})



def home(request):
    return render(request, 'app/index.html', {})
