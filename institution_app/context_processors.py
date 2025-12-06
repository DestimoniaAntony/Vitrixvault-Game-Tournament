from .models import Event
from staff_app.models import Institution

def event_context(request):
    try:
        if request.user.is_authenticated:
            institution = Institution.objects.get(user=request.user)
            events = Event.objects.filter(created_by=institution)
        else:
            events = Event.objects.none()
    except Institution.DoesNotExist:
        events = Event.objects.none()
    
    return {
        'events': events
    }