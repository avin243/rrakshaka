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
    if request.method == 'POST':
        report_id = request.POST.get('report_id')
        new_status = request.POST.get('status')
        admin_notes = request.POST.get('admin_notes')
        
        if report_id:
            report = get_object_or_404(IssueReport, id=report_id)
            report.status = new_status
            report.admin_notes = admin_notes
            report.save()
            messages.success(request, f'Status updated to {new_status} for Issue #{report.id}')
            return redirect('reviewer_dashboard')
            
    reports = IssueReport.objects.all().order_by('-created_at')
    status_choices = IssueReport.STATUS_CHOICES
    
    context = {
        'reports': reports,
        'status_choices': status_choices,
    }
    return render(request, 'core/reviewer_dashboard.html', context)
