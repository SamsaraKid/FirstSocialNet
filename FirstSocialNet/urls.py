"""
URL configuration for FirstSocialNet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from socialapp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('registration/', views.registration, name='registration'),
    path('user/', include('django.contrib.auth.urls')),
    path('login/', views.index, name='login'),

    # path('<slug:slug>/', views.ProfileDetail.as_view(), name='profile'),
    path('subscribe', views.subscribe, name='subscribe'),
    path('unsubscribe', views.unsubscribe, name='unsubscribe'),
    path('delpost/<int:id>', views.delpost, name='delpost'),
    path('news/', views.NewsList.as_view(), name='news'),
    path('peoplesearch/', views.peoplesearch, name='peoplesearch'),
    path('<slug:slug>/', views.profiledetail, name='profile'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
