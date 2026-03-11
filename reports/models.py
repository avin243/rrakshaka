from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    icon_class = models.CharField(max_length=50, blank=True, null=True, help_text="CSS class for icon")
    
    class Meta:
        verbose_name_plural = "Categories"
        
    def __str__(self):
        return self.name

class IssueReport(models.Model):
    SEVERITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    STATUS_CHOICES = [
        ('Submitted', 'Submitted'),
        ('Acknowledged', 'Acknowledged'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Rejected', 'Rejected/Spam'),
    ]

    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    photo = models.ImageField(upload_to='report_photos/')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='Low')
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Submitted')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Issue #{self.id} - {self.category} ({self.status})"
        
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_status = None
        if not is_new:
            try:
                old_report = IssueReport.objects.get(pk=self.pk)
                old_status = old_report.status
            except IssueReport.DoesNotExist:
                pass
                
        super().save(*args, **kwargs)
        
        # Globally handle point updates on status changes
        if not is_new and old_status and old_status != self.status:
            from accounts.models import RewardPoint
            try:
                profile = self.reporter.profile
                if self.status == 'Resolved':
                    profile.points += 20
                    profile.save()
                    RewardPoint.objects.create(
                        user=self.reporter,
                        points=20,
                        action=f"Issue '{self.category.name}' marked as Resolved"
                    )
                elif self.status == 'Rejected':
                    profile.points -= 15
                    profile.save()
                    RewardPoint.objects.create(
                        user=self.reporter,
                        points=-15,
                        action=f"Issue '{self.category.name}' rejected as Spam"
                    )
            except Exception:
                pass

class ReportImage(models.Model):
    report = models.ForeignKey(IssueReport, on_delete=models.CASCADE, related_name='extra_images')
    image = models.ImageField(upload_to='report_photos/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for Issue #{self.report.id}"
