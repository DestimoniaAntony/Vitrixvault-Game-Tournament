from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from institution_app.forms import EventForm, MatchScoreForm, StudentRegistrationForm
from institution_app.models import Event, Match, Student, Team
from staff_app.models import Institution
# Create your views here.


def index(request):
    return render(request, 'institute/index.html')


def event_list(request):
    try:
        institution = Institution.objects.get(user=request.user)
        events = Event.objects.filter(created_by=institution)
    except Institution.DoesNotExist:
        events = Event.objects.none()  # No events if user has no institution

    return render(request, 'institute/events/event_list.html', {'events': events})

@login_required
def add_event(request):
    institution = get_object_or_404(Institution, user=request.user)  # Assuming Institution is linked to User
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = institution  # Assign the institution instead of user
            event.save()
            messages.success(request, "Event added successfully!")
            return redirect('event_list')
    else:
        form = EventForm()
    
    return render(request, 'institute/events/add_event.html', {'form': form})
@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.user != event.created_by.user:  
        messages.error(request, "You are not authorized to edit this event.")
        return redirect('event_list')

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect('event_list')
    else:
        form = EventForm(instance=event)

    return render(request, 'institute/events/edit_event.html', {'form': form, 'event': event})
@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    messages.success(request, "Event deleted successfully!")
    return redirect('event_list')



# def register_student(request, student_id=None):
#     try:
#         # Get the institution linked to the logged-in user
#         institution = Institution.objects.get(user=request.user)
#     except Institution.DoesNotExist:
#         messages.error(request, "You are not associated with any institution.")
#         return redirect('login')  # Redirect to login if no institution is found for the user

#     # If student_id is provided, we are editing an existing student
#     if student_id:
#         student = get_object_or_404(Student, id=student_id)

#         # Ensure the student belongs to the logged-in institution
#         if student.institution != institution:
#             messages.error(request, "You do not have permission to edit this student.")
#             return redirect('student_list')  # Redirect to the student list page

#         form = StudentRegistrationForm(request.POST or None, instance=student, institution=institution)

#     else:
#         # We are registering a new student
#         form = StudentRegistrationForm(request.POST or None, institution=institution)

#     # Check if the form is valid and save data
#     if form.is_valid():
#         if student_id:
#             # Update the existing student
#             student = form.save(commit=False)

#             # Update the related User model (first_name, last_name, email)
#             user = student.user
#             user.first_name = form.cleaned_data['first_name']
#             user.last_name = form.cleaned_data['last_name']
#             user.email = form.cleaned_data['email']
            
#             # If password is provided, update the password
#             if form.cleaned_data['password']:
#                 user.set_password(form.cleaned_data['password'])  # Hash the new password
            
#             # Save the user
#             user.save()

#             # Save the student
#             student.save()

#             # Assign the student to events
#             student.events.set([event.id for event in form.cleaned_data['event']])


#             # Auto-assign student to teams
#             for event in form.cleaned_data['event']:
#                 assign_student_to_team(request, student, event.id)

#             messages.success(request, "Student details updated successfully!")

#         else:
#             # Register a new student
#             user = User.objects.create_user(
#                 username=form.cleaned_data['username'],
#                 first_name=form.cleaned_data['first_name'],
#                 last_name=form.cleaned_data['last_name'],
#                 email=form.cleaned_data['email'],
#                 password=form.cleaned_data['password']  # Password is hashed automatically
#             )

#             student = Student.objects.create(
#                 user=user,
#                 institution=institution,
#                 phone=form.cleaned_data['phone'],
#                 address=form.cleaned_data['address'],
#                 date_of_birth=form.cleaned_data['date_of_birth'],
#                 roll_number=form.cleaned_data['roll_number'],
#                 course=form.cleaned_data['course']
#             )

#             # Assign the student to events
#             student.events.set(form.cleaned_data['event'])

#             # Auto-assign student to teams
#             for event in form.cleaned_data['event']:
#                 assign_student_to_team(request, student, event.id)

#             messages.success(request, "Student registered successfully!")

#         # Redirect to the list of students after success
#         return redirect('student_list')

#     # If the form is invalid, return the form with errors
#     return render(request, 'institute/students/add_student.html', {
#         'form': form,
#         'student': student if student_id else None  # Pass student to template for editing purposes
#     })


def register_student(request, student_id=None):
    try:
        # Get the institution linked to the logged-in user
        institution = Institution.objects.get(user=request.user)
    except Institution.DoesNotExist:
        messages.error(request, "You are not associated with any institution.")
        return redirect('login')  # Redirect to login if no institution is found for the user

    student = None  # Initialize student variable
    if student_id:
        student = get_object_or_404(Student, id=student_id)

        # Ensure the student belongs to the logged-in institution
        if student.institution != institution:
            messages.error(request, "You do not have permission to edit this student.")
            return redirect('student_list')  # Redirect to the student list page

        form = StudentRegistrationForm(request.POST or None, instance=student, institution=institution)
    else:
        form = StudentRegistrationForm(request.POST or None, institution=institution)

    if form.is_valid():
        if student_id:
            student = form.save(commit=False)
            user = student.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']

            if form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])  # Hash password
            
            user.save()
            student.save()
            student.events.set(form.cleaned_data['event'])  # Assign only institution's events

            for event in form.cleaned_data['event']:
                assign_student_to_team(request, student, event.id)

            messages.success(request, "Student details updated successfully!")
        else:
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )

            student = Student.objects.create(
                user=user,
                institution=institution,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                date_of_birth=form.cleaned_data['date_of_birth'],
                roll_number=form.cleaned_data['roll_number'],
                course=form.cleaned_data['course']
            )

            student.events.set(form.cleaned_data['event'])  # Assign only institution's events

            for event in form.cleaned_data['event']:
                assign_student_to_team(request, student, event.id)

            messages.success(request, "Student registered successfully!")

        return redirect('student_list')

    return render(request, 'institute/students/add_student.html', {
        'form': form,
        'student': student if student_id else None
    })



def assign_student_to_team(request, student, event_id):  
    event = get_object_or_404(Event, id=event_id)  # Expecting event ID, not an instance
    students = list(event.students.all())  # Get registered students
    team_size = event.team_size  # Team size from event model
    
    if not team_size or team_size <= 0:
        messages.error(request, "Invalid team size for this event.")  # Now request is defined
        return
    
    Team.objects.filter(event=event).delete()  # Clear old teams
    teams = [students[i:i + team_size] for i in range(0, len(students), team_size)]
    
    for index, members in enumerate(teams, start=1):
        team = Team.objects.create(event=event, team_number=index)
        team.members.set(members)  # Assign students to this team
    
    messages.success(request, f"Teams assigned for {event.name} successfully!")




def event_teams_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    teams = event.teams.all().order_by("team_number")

    return render(request, 'institute/events/teams.html', {'event': event, 'teams': teams})



def student_list(request):
    institution = get_object_or_404(Institution, user=request.user)
    students = Student.objects.filter(institution=institution)
    return render(request, 'institute/students/student_list.html', {'students': students})


def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    user = student.user  # Get the associated auth_user record

    student.delete()  # Delete from Student model
    user.delete()  # Delete from User model

    messages.success(request, "Student deleted successfully!")
    return redirect('student_list')




# def create_match(request):
#     if request.method == "POST":
#         form = MatchForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('match_list')  # Redirect to match listing page
#     else:
#         form = MatchForm()

#     return render(request, "institute/create_match.html", {"form": form})


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    teams = Team.objects.filter(event=event)
    matches = Match.objects.filter(event=event)

    return render(request, 'institute/event_detail.html', {
        'event': event,
        'teams': teams,
        'matches': matches
    })



def generate_matches(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    teams = list(Team.objects.filter(event=event))

    if len(teams) < 2:
        messages.error(request, "Not enough teams to generate matches.")
        return redirect('event_detail', event_id=event_id)

    if Match.objects.filter(event=event).exists():
        messages.warning(request, "Matches already generated for this event.")
        return redirect('match_list')

    match_count = 0
    for i in range(0, len(teams) - 1, 2):
        Match.objects.create(
            event=event,
            team1=teams[i],
            team2=teams[i + 1],
            status="Upcoming"
        )
        match_count += 1

    messages.success(request, f"{match_count} matches generated successfully!")
    return redirect('match_list')



def match_list(request):
    try:
        institution = Institution.objects.get(user=request.user)
        # Get all events created by this institution
        institution_events = Event.objects.filter(created_by=institution)
        # Get matches only from those events
        matches = Match.objects.filter(event__in=institution_events)
    except Institution.DoesNotExist:
        matches = Match.objects.none()
    
    return render(request, 'institute/match_list.html', {'matches': matches})



def update_match_score(request, match_id):
    match = get_object_or_404(Match, id=match_id)

    if request.method == "POST":
        form = MatchScoreForm(request.POST, instance=match)
        if form.is_valid():
            form.save()
            return redirect('match_list')  # Redirect to match list page after updating

    else:
        form = MatchScoreForm(instance=match)

    return render(request, 'institute/update_match_score.html', {'form': form, 'match': match})