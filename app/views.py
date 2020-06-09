from django.db.models.functions import Coalesce
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Project, Blog, Education

from .forms import BlogForm, EducationForm

from django.shortcuts import redirect


def project_list(request):
    projects = Project.objects.order_by('-published_date')
    return render(request, 'app/portfolio_list.html', {'projects': projects})


def home(request):
    return render(request, 'app/home.html', {})


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'app/portfolio_detail.html', {'project': project})


def blog_list(request):
    blogs = Blog.objects.raw('SELECT * FROM app_blog ORDER BY published_date DESC')
    return render(request, 'app/blog_list.html', {'blogs': blogs})


def cv(request):
    educations = Education.objects.order_by('-end_year')
    return render(request, 'app/cv.html', {'educations': educations})


def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    return render(request, 'app/blog_detail.html', {'blog': blog})


def blog_new(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog_detail', pk=post.pk)
    else:
        form = BlogForm()
    return render(request, 'app/blog_new.html', {'form': form})


def cv_education_new(request):
    educations = Education.objects.order_by('-end_year')
    if request.method == "POST":
        form = EducationForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.start_year = request.POST.get("start_year")
            post.end_year = request.POST.get("end_year")
            post.save()
            return redirect('cv')
    else:
        form = EducationForm()
    return render(request, 'app/cv_education_edit.html', {'form': form, 'educations': educations})


def cv_education_edit(request, pk):
    post = get_object_or_404(Education, pk=pk)
    educations = Education.objects.order_by('-end_year')
    if request.method == "POST":
        form = EducationForm(request.POST, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            post.start_year = request.POST.get("start_year")
            post.end_year = request.POST.get("end_year")
            post.save()
            return redirect('cv')
    else:
        form = EducationForm()
    return render(request, 'app/cv_education_edit.html', {'form': form, 'educations': educations})
