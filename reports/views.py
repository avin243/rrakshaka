from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import IssueReportForm
from .models import IssueReport
from accounts.models import RewardPoint

@login_required
def create_report(request):
    if request.method == 'POST':
        form = IssueReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.save()
            
            # Award points
            try:
                profile = request.user.profile
                profile.points += 10
                profile.save()
                RewardPoint.objects.create(
                    user=request.user,
                    points=10,
                    action='Reported an issue'
                )
            except:
                pass

            return redirect('report_success', report_id=report.id)
    else:
        form = IssueReportForm()
    
    return render(request, 'reports/create_report.html', {'form': form})

@login_required
def report_success(request, report_id):
    report = get_object_or_404(IssueReport, id=report_id, reporter=request.user)
    return render(request, 'reports/report_success.html', {'report': report})

def public_map(request):
    reports = IssueReport.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True)
    return render(request, 'reports/public_map.html', {'reports': reports})
