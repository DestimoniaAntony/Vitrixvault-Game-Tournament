
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Victrix_app import views

urlpatterns = [
    
    path('', views.index , name='index'),
    path('EventBoard', views.EventBoard , name='EventBoard'),
    path('register_staff', views.register_staff, name='register_staff'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('Match_results', views.Match_results, name='Match_results'),
]
if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)