
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from admin_app import views

urlpatterns = [
    
    path('', views.index , name='admin_index'),
    path('staff_list', views.staff_list , name='staff_list'),
    path('approve/<int:staff_id>/', views.approve_staff, name='approve_staff'),
    path('reject_staff/<int:staff_id>/', views.reject_staff, name='reject_staff'),
    path('All_Match_results', views.All_Match_results, name='All_Match_results'),
    
]
if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)