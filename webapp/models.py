from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.username

class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Internship(models.Model):
    title = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='internships')
    location = models.CharField(max_length=100)
    stipend = models.CharField(max_length=100)
    skills = models.CharField(
        max_length=250,help_text="Comma-separated list of required skills",blank=True, 
    )
    description = models.TextField()
    posted_date = models.DateTimeField(auto_now_add=True)  # add this
    
    def __str__(self):
        return f"{self.title} at {self.company.name}"
    
class InternshipApplication(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE, related_name='applications')
    applied_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'internship')  # Prevent duplicate applications

    STATUS_CHOICES = [
        ('pending', 'Under Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='applications'
    )
    internship = models.ForeignKey(
        'Internship', 
        on_delete=models.CASCADE, 
        related_name='applications'
    )
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    rejection_reason = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'internship')

    def __str__(self):
        return f"{self.user} → {self.internship.title}"

    def get_status_display(self):
        """Return human-readable status"""
        status_dict = dict(self.STATUS_CHOICES)
        return status_dict.get(self.status, self.status)


