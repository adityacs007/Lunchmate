from django.conf.urls import patterns, include, url
from . import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
   url(r'^$', views.home, name='home'),
   url(r'^index/', views.index, name='index'),
   url(r'^adi/',views.adi_test),
   url(r'^adi/',views.adi, name='adi'),
   url('', include('social.apps.django_app.urls', namespace='social')),
   url('', include('django.contrib.auth.urls', namespace='auth')),
   url(r'^admin/', include(admin.site.urls)),
]
