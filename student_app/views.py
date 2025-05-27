from django.shortcuts import get_object_or_404, render

from institution_app.models import Match, Student

# from institution_app.models import Student

# Create your views here.


def index(request):
    return render(request, 'student/index.html')

def student_events(request):
    student = get_object_or_404(Student, user=request.user)
    events = student.events.all()  # Get all registered events

    context = {
        'student': student,
        'events': events,  # Pass the event list to the template
    }
    return render(request, 'student/student_events.html', context)


def student_profile(request):
    student = request.user.student  

    # Fetch teams and events correctly
    teams = student.teams.select_related("event")  
    events = student.events.all()  

    # Fetch all matches where the student's team is involved
    matches = Match.objects.filter(team1__in=teams) | Match.objects.filter(team2__in=teams)

    # Determine winners (store in a dictionary for easy lookup)
    winners_dict = {}
    for match in matches:
        if match.status == "Finished":
            if match.score_team1 > match.score_team2:
                winners_dict[match.team1.id] = True
            elif match.score_team1 < match.score_team2:
                winners_dict[match.team2.id] = True

    context = {
        "student": student,
        "events": events,
        "teams": teams,
        "competitions": events,  
        "matches": matches,
        "winners_dict": winners_dict,  # Use this in template
    }
    return render(request, "student/profile.html", context)


def my_matches(request):
    student = Student.objects.get(user=request.user)  # Get the logged-in student
    my_teams = student.teams.all()  # Get all teams the student is part of
    matches = Match.objects.filter(team1__in=my_teams) | Match.objects.filter(team2__in=my_teams)  # Filter matches
    
    return render(request, "student/my_matches.html", {"matches": matches, "my_teams": my_teams})




# def student_dashboard(request):
#     student = request.user  # Get the logged-in student
#     competitions = student.teams.all()  # Fetch competitions the student is part of

#     context = {
#         "student": student,
#         "competitions": competitions
#     }
#     return render(request, "student/dashboard.html", context)