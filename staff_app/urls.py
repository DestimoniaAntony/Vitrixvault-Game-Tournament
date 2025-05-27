
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from staff_app import views

urlpatterns = [
    
    path('', views.index , name='staff_index'),

    path('add_institution/', views.add_institution, name='add_institution'),
    path('edit_institution/<int:institution_id>/', views.edit_institution, name='edit_institution'),
    path('delete_institution/<int:institution_id>/', views.delete_institution, name='delete_institution'),
    path('institution_list/', views.institution_list, name='institution_list'),
    

    
]
if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)