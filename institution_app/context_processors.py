from .models import Event

def event_context(request):
    return {
        'events': Event.objects.all()
    }