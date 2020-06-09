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
    path('cv/edit/education/new/', views.cv_education_new, name='cv_new'),
    path('cv/edit/education/<int:pk>/', views.cv_education_edit, name='cv_edit'),

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
