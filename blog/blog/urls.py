"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django.conf.urls import url
from . import  settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # Step 7 : Add Url Route for apps
    path('',include("normaluser.urls")),
    path('blog-admin/',include("adminuser.urls"),name="newadmin")
]

# Step 5 : Setup this for our local mode in development
# So that we can access files in media folder
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

#Step 6 : Setup to access static file in debug mode
    urlpatterns += staticfiles_urlpatterns()
