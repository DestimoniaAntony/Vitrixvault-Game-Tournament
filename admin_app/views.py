from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from Victrix_app.models import Staff
from institution_app.models import Event, Match
from staff_app.models import Institution

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


def institution_list(request):
    institutions = Institution.objects.all().select_related('created_by', 'created_by__user')
    return render(request, 'admin/institution_list.html', {'institutions': institutions})


def institution_games(request, institution_id):
    institution = get_object_or_404(Institution, id=institution_id)
    games = Event.objects.filter(created_by=institution)
    return render(request, 'admin/institution_games.html', {
        'institution': institution,
        'games': games
    })