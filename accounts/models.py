from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    city_ward = models.CharField(max_length=100, blank=True, null=True)
    terms_accepted = models.BooleanField(default=False)
    points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class RewardPoint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rewards')
    points = models.IntegerField()
    action = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.points} to {self.user.username} for {self.action}"
