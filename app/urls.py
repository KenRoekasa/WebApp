from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/', views.blog_list, name='blog'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('portfolio/', views.project_list, name='portfolio_list'),
    path('portfolio/<int:pk>/', views.project_detail, name='portfolio_detail'),
    path('cv/', views.cv, name='cv'),
    path('blog/new/', views.blog_new, name='blog_new'),
    path('blog/edit/<int:pk>/', views.blog_edit, name='blog_edit'),
    path('cv/edit/education/new/', views.cv_education_new, name='cv_education_new'),
    path('cv/edit/education/<int:pk>/', views.cv_education_edit, name='cv_education_edit'),
    path('cv/edit/techskills/new/', views.cv_tech_skills_new, name='cv_tech_skils_new'),
    path('cv/edit/techskills/<int:pk>/', views.cv_tech_skills_edit, name='cv_tech_skils_edit'),
    path('cv/edit/workexp/new/', views.cv_work_exp_new, name='cv_work_experience_new'),
    path('cv/edit/workexp/<int:pk>/', views.cv_work_exp_edit, name='cv_work_experience_edit'),
    path('cv/edit/projects/new/', views.cv_projects_new, name='cv_project_new'),
    path('cv/edit/projects/<int:pk>/', views.cv_projects_edit, name='cv_project_edit'),

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
