from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from .models import Internship,InternshipApplication

User = get_user_model()  


def register_page(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        role = request.POST.get('role', '').strip()

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
        )

        if role == 'admin':
            user.is_staff = True
            user.is_superuser=True
            user.is_active = True
            user.save()
        login(request,user)

        if role == 'admin':
            return redirect(reverse('admin:index'))
        else:
            return redirect('user_dashboard')

    return render(request, 'register.html')


def login_page(request):

    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user_role = request.POST.get('role','').strip()

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.role != user_role:
                raise PermissionDenied
            login(request, user)

            if user.role == 'admin':
                return redirect(reverse('admin:index'))
            else:
                return redirect('user_dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

def is_admin(user):
    """Check if user is admin with proper permissions"""
    if not user.is_authenticated:
        return False
    return user.role == 'admin' and user.is_staff

def is_user(user): 
    """Check if user has regular user role"""
    if not user.is_authenticated:
        return False
    return user.role == 'user' and not user.is_staff


@login_required
@user_passes_test(is_user)                    # keep your role-check
def user_dashboard(request):
    qs = Internship.objects.select_related('company')

    # ── read GET parameters ─────────────────────────────────────────
    role     = request.GET.get('role', '').strip()
    skills   = request.GET.get('skills', '').strip()
    location = request.GET.get('location', '').strip()
    stipend  = request.GET.get('stipend', '')

    filters = Q()
    if role:
        filters &= Q(title__icontains=role)
    if skills:
        filters &= Q(skills__icontains=skills)  # or another skills field
    if location:
        filters &= Q(location__icontains=location)
    if stipend.isdigit():
        filters &= Q(stipend__gte=int(stipend))  # use an IntegerField for stipend


    internships = qs.filter(filters)

    # which internships the current user already applied to
    applied_ids = InternshipApplication.objects.filter(
        user=request.user).values_list('internship_id', flat=True)

    context = {
        'internships': internships,
        'applied_internship_ids': applied_ids,
    }
    return render(request, 'user_dashboard.html', context)

@login_required
def apply_internship(request, internship_id):
    internship = get_object_or_404(Internship, pk=internship_id)
    
    # Check if already applied
    application,created = InternshipApplication.objects.get_or_create(
        user=request.user,
        internship=internship
    )
    if created:
        messages.success(request, f"You have successfully applied to {internship.title}.")
    else:
        messages.info(request, f"You have already applied to {internship.title}.")

    return redirect('user_dashboard')

@login_required
@user_passes_test(is_user)
def applied_internships(request):
    applications = InternshipApplication.objects.filter(
        user=request.user
    ).select_related('internship', 'internship__company')
    
    context = {
        'user': request.user,
        'applications': applications,
    }
    return render(request, 'applied.html', context)

@login_required
@user_passes_test(is_user)
def progress(request):
    applications = (
        InternshipApplication.objects
        .filter(user=request.user)
        .select_related('internship', 'internship__company')
        .order_by('-applied_at')
    )
    
    # Calculate statistics with proper logic
    total_applications = applications.count()
    try:
        pending_applications = applications.filter(status='pending').count()
        accepted_applications = applications.filter(status='accepted').count()
        rejected_applications = applications.filter(status='rejected').count()
    except:
        # Fallback if status field doesn't exist
        pending_applications = total_applications
        accepted_applications = 0
        rejected_applications = 0
    
    context = {
        'applications': applications,
        'total_applications': total_applications,
        'pending_applications': pending_applications,  # This is "Under Review"
        'accepted_applications': accepted_applications,
        'rejected_applications': rejected_applications,
    }
    
    return render(request, 'progress.html', context)

def custom_permission_denied_view(request, exception=None):
    return render(request, "403.html", {
        'exception': exception,
        'user': request.user,
        'error_message': str(exception) if exception else "Access denied"
    }, status=403)




