from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='index'),
    path('portfolio/', views.project_list, name='portfolio_list'),
    path('portfolio/<int:pk>',views.project_detail,name='portfolio_detail'),

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)