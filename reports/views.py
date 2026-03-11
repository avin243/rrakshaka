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
            
            # The first photo is bound to the form and will be saved to report.photo
            report.save()
            
            # Handle additional photos
            photos = request.FILES.getlist('photo')
            extra_photos_count = 0
            
            if len(photos) > 1:
                # The first one is already saved in report.photo by the form
                # Save the rest in ReportImage
                from .models import ReportImage
                for photo in photos[1:]:
                    ReportImage.objects.create(report=report, image=photo)
                    extra_photos_count += 1
            
            # Award points
            try:
                base_points = 10
                extra_points = extra_photos_count * 5
                total_points = base_points + extra_points
                
                profile = request.user.profile
                profile.points += total_points
                profile.save()
                
                action_text = 'Reported an issue'
                if extra_photos_count > 0:
                    action_text += f' (with {extra_photos_count} extra photos)'
                    
                RewardPoint.objects.create(
                    user=request.user,
                    points=total_points,
                    action=action_text
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
    from .models import Category
    reports = IssueReport.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True).exclude(status__in=['Resolved', 'Rejected'])
    categories = Category.objects.all()
    return render(request, 'reports/public_map.html', {'reports': reports, 'categories': categories})
