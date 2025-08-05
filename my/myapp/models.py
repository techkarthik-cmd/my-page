# my/myapp/models.py
from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, unique=True, blank=True)
    headline = models.CharField(max_length=140, blank=True)  # e.g., "AWS Data Engineer"
    summary = models.TextField(blank=True)  # about you
    skills = models.TextField(blank=True)   # comma-separated or free text
    experience = models.TextField(blank=True)  # previous experience details
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return f"Profile: {self.user.get_full_name() or self.user.username}"

class OTPCode(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    phone = models.CharField(max_length=20)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.phone} - {self.code}"


class Project(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    short_desc = models.CharField(max_length=180, blank=True)
    description = models.TextField()
    tech_stack = models.CharField(max_length=240, help_text="Comma separated: Django, n8n, PySpark")
    repo_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    cover = models.ImageField(upload_to='projects/', blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} <{self.email}>'

