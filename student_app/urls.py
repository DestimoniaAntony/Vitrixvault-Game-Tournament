
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from student_app import views

urlpatterns = [
    
    path('', views.index , name='student_index'),
    path('student_events', views.student_events, name='student_events'),
    path('student_profile', views.student_profile, name='student_profile'),
    path('my_matches', views.my_matches, name='my_matches'),
    
]
if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)