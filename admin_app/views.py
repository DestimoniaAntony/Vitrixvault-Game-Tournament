from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from Victrix_app.models import Staff
from institution_app.models import Event, Match

# Create your views here.


def index(request):
    return render(request, 'admin/index.html')

def staff_list(request):
    staff_members = Staff.objects.all()
    return render(request, 'admin/staff_list.html', {'staff_members': staff_members})

def approve_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    staff.is_active = True
    staff.user.is_active = True
    staff.user.save()
    staff.save()
    return redirect('staff_list')

def reject_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    username = staff.user.username
    staff.user.delete()  # Deletes both Staff and associated User
    messages.error(request, f"Staff {username} has been rejected and removed.")
    return redirect('staff_list')

from django.utils.timezone import now
def All_Match_results(request):
    events = Event.objects.all().order_by('date')
    matches = Match.objects.all().order_by('-start_time')

    context = {
        'events': events,
        'matches': matches,
        'today': now().date(),
    }
    return render(request, 'admin/match_results.html', context)