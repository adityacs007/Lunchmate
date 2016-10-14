from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin
from . import views
from views import HomeView

urlpatterns = [    
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r"^addfriend/$", views.add_friend, name="add_friend"),
    url(r"^home/$", views.home, name="home"),
    url(r'^friendship/friend/add/(?P<to_username>[\w-]+)/', views.add_friend),
    url(r'^friendship/', include('friendship.urls')),
    url(r"^index/", views.index, name="index"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
