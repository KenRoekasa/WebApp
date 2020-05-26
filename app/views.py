from django.shortcuts import render, get_object_or_404
from .models import Project, Blog


# Create your views here.
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'app/portfolio_list.html', {'projects': projects})


def home(request):
    return render(request, 'app/home.html', {})


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'app/portfolio_detail.html', {'project': project})


def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'app/blog_list.html', {'blogs': blogs})
