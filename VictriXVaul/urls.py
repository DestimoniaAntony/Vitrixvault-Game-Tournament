"""
URL configuration for VictriXVaul project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('admin/', include('admin_app.urls')),
    path('staff/', include('staff_app.urls')),
    path('student/', include('student_app.urls')),
    path('institution/', include('institution_app.urls')),
    path('', include('Victrix_app.urls')),
]
# Add static and media URL patterns. In development Django serves these
# automatically when DEBUG=True. Adding them here ensures the files are
# available when using runserver or the --insecure flag. Do NOT rely on
# Django to serve static files in production; use a web server or WhiteNoise.
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom error handlers (templates `404.html` and `500.html` in project `templates/` folder)
# These are used when DEBUG is False.
handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'