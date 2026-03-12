from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from reports.models import IssueReport
def home(request):
    return render(request, 'core/index.html')

def dashboard(request):
    return render(request, 'core/dashboard.html')

def rewards(request):
    return render(request, 'core/rewards.html')

@login_required
@user_passes_test(lambda u: u.is_staff)
def reviewer_dashboard(request):
    from accounts.models import Profile
    if request.method == 'POST':
        report_id = request.POST.get('report_id')
        new_status = request.POST.get('status')
        admin_notes = request.POST.get('admin_notes')
        
        profile_id = request.POST.get('profile_id')
        action = request.POST.get('action')
        
        if report_id:
            report = get_object_or_404(IssueReport, id=report_id)
            
            # Permission check: Only superusers or the assigned staff member can edit
            if not request.user.is_superuser and report.assigned_to != request.user:
                messages.error(request, "You are not authorized to edit this report.")
                return redirect('reviewer_dashboard')
                
            report.status = new_status
            report.admin_notes = admin_notes
            report.save()
            
            messages.success(request, f'Status updated to {new_status} for Issue #{report.id}')
            return redirect('reviewer_dashboard')
            
    # Filter reports based on user role
    if request.user.is_superuser:
        reports = IssueReport.objects.all().order_by('-created_at')
    else:
        reports = IssueReport.objects.filter(assigned_to=request.user).order_by('-created_at')
        
    status_choices = IssueReport.STATUS_CHOICES
    
    context = {
        'reports': reports,
        'status_choices': status_choices,
    }
    return render(request, 'core/reviewer_dashboard.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_staff_management(request):
    from accounts.models import Profile
    from django.contrib.auth.models import User
    
    if request.method == 'POST':
        profile_id = request.POST.get('profile_id')
        action = request.POST.get('action')
        
        if profile_id:
            profile = get_object_or_404(Profile, id=profile_id)
            if action == 'approve':
                profile.is_staff_member = True
                profile.is_pending_staff_approval = False
                # Also grant Django staff status for login permissions
                profile.user.is_staff = True
                profile.user.save()
                profile.save()
                messages.success(request, f"Approved {profile.user.username} as staff member.")
            elif action == 'reject':
                profile.is_pending_staff_approval = False
                profile.save()
                messages.error(request, f"Rejected staff application for {profile.user.username}.")
            return redirect('admin_staff_management')

    pending_staff = Profile.objects.filter(is_pending_staff_approval=True)
    approved_staff = Profile.objects.filter(is_staff_member=True)
    
    context = {
        'pending_staff': pending_staff,
        'approved_staff': approved_staff,
    }
    return render(request, 'core/admin_staff_management.html', context)
