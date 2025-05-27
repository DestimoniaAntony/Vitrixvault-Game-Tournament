from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from Victrix_app.models import Staff
from staff_app.forms import InstitutionEditForm, InstitutionForm
from staff_app.models import Institution
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    return render(request, 'staff/index.html')

def add_institution(request):
    if request.method == "POST":
        form = InstitutionForm(request.POST)
        if form.is_valid():
            institution = form.save(commit=False)

            # Check if user exists, otherwise create a new one
            registering_username = form.cleaned_data.get('username')
            registering_email = form.cleaned_data.get('email')

            user, created = User.objects.get_or_create(
                username=registering_username, 
                defaults={'email': registering_email}
            )
            institution.user = user  # Assign the created/retrieved user

            # Fetch Staff instance for the logged-in user
            try:
                staff = Staff.objects.get(user=request.user)
                institution.created_by = staff  # Assign the staff who created it
            except Staff.DoesNotExist:
                messages.error(request, "You must be a staff member to add an institution.")
                return redirect('institution_list')

            institution.save()
            messages.success(request, "Institution added successfully!")
            return redirect('institution_list')
    else:
        form = InstitutionForm()

    return render(request, 'staff/add_institution.html', {'form': form})


def edit_institution(request, institution_id):
    institution = get_object_or_404(Institution, id=institution_id)

    # Ensure only the staff member who created the institution can edit
    if not hasattr(request.user, 'staff') or request.user.staff != institution.created_by:
        messages.error(request, "You do not have permission to edit this institution.")
        return redirect('institution_list')

    if request.method == "POST":
        form = InstitutionEditForm(request.POST, instance=institution)
        if form.is_valid():
            form.save()
            messages.success(request, "Institution details updated successfully!")
            return redirect('institution_list')
    else:
        form = InstitutionEditForm(instance=institution)

    return render(request, 'staff/edit_institution.html', {'form': form, 'institution': institution})



# Delete Institution
def delete_institution(request, institution_id):
    institution = get_object_or_404(Institution, id=institution_id, user=request.user)
    institution.delete()
    messages.success(request, "Institution deleted successfully!")
    return redirect('institution_list')
def institution_list(request):
    try:
        # Fetch the logged-in staff
        staff = Staff.objects.get(user=request.user)
        
        # Filter institutions created by this staff
        institutions = Institution.objects.filter(created_by=staff)
        
        # Check if the staff has created any institutions
        if not institutions:
            messages.info(request, "You have not created any institutions yet.")
    
    except Staff.DoesNotExist:
        messages.error(request, "You must be a staff member to view this page.")
        return redirect('index')  # Redirect to home or an appropriate page

    # Render the institutions in the template
    return render(request, 'staff/institution_list.html', {'institutions': institutions})



