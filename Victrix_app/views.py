from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

# from institution_app.models import Student
from institution_app.models import Event, Match, Student
from staff_app.models import Institution
from .forms import UserLoginForm
from Victrix_app.forms import StaffRegistrationForm

# Create your views here.



def index(request):
    return render(request, 'index.html')

def EventBoard(request):
    public_events = Event.objects.filter(visibility=True)  # Fetch only public events

    context = {
        'public_events': public_events,
    }
    return render(request, 'events.html', context)



def register_staff(request):
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = StaffRegistrationForm()
    return render(request, 'staff_register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        
        if form.is_valid():
            # Extract cleaned data from the form
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Authenticate user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Check if the user is active
                if not user.is_active:
                    messages.error(request, "Your account is inactive. Please contact support.")
                    return redirect('login')  # Redirect back to login page

                # Superuser (Admin) Login
                if user.is_superuser:
                    login(request, user)
                    return redirect('admin_index')  # Redirect to admin dashboard

                # Staff Login (Check if the user has a related Staff object)
                elif hasattr(user, 'staff') and user.staff.is_active:
                    login(request, user)
                    return redirect('staff_index')  # Redirect to staff dashboard
                elif hasattr(user, 'staff'):
                    messages.error(request, "Your staff account is not yet approved.")
                
                elif Institution.objects.filter(user=user).exists():
                    login(request, user)
                    return redirect('institution_index')
                
                elif Student.objects.filter(user=user).exists():
                    login(request, user)
                    return redirect('student_index')
                
                
                else:
                    messages.error(request, "Invalid login credentials.")  # Invalid user role or missing related objects

            else:
                messages.error(request, "Invalid username or password.")  # Invalid username or password
        else:
            messages.error(request, "Invalid form submission.")  # If form is not valid

    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})




def user_logout(request):
    logout(request)
    return redirect('login')

from django.utils.timezone import now

def Match_results(request):
    events = Event.objects.all().order_by('date')
    matches = Match.objects.all().order_by('-start_time')

    context = {
        'events': events,
        'matches': matches,
        'today': now().date(),
    }
    return render(request, 'match_results.html', context)