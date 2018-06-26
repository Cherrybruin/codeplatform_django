"""codeplatform_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from Code_Platform import views
urlpatterns = [
    path(r'', views.index),
    path(r'admin/', admin.site.urls),
    path(r'register/', views.user_register),
    path(r'login', views.user_login),
    path(r'logout/', views.user_logout),
    path(r'download/<str:username>/<str:projectname>/<path:fpath>', views.user_project_download),
    path(r'<str:username>/start', views.project_start),
    # path(r'user/', views.user_index),
    path(r'<str:username>/', views.user_index),
    path(r'<str:username>/<str:projectname>', views.user_project),
    path(r'<str:username>/<str:projectname>/uploadfile', views.user_project),

    path(r'<str:username>/<str:projectname>/<path:fpath>', views.user_project),
]
