
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from institution_app import views

urlpatterns = [
    
    path('', views.index , name='institution_index'),
    

    path('events/', views.event_list, name='event_list'),
    path('events/add/', views.add_event, name='add_event'),
    path('events/edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('events/delete/<int:event_id>/', views.delete_event, name='delete_event'),


    path('add_student/', views.register_student, name='add_student'),
    path('student_list/', views.student_list, name='student_list'),
    path('edit_student/<int:student_id>/', views.register_student, name='edit_student'),
    path('delete_student/<int:student_id>/', views.delete_student, name='delete_student'),


    path('event/<int:event_id>/teams/', views.event_teams_view, name='event_teams_view'),
    path('event/<int:event_id>/assign_teams/', views.assign_student_to_team, name='assign_student_to_team'),

    path('generate_matches/<int:event_id>/', views.generate_matches, name='generate_matches'),
    path('matches/', views.match_list, name='match_list'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('match/<int:match_id>/update/', views.update_match_score, name='update_match_score'),
]
if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)