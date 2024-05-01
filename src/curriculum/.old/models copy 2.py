from django.db import models
from account.models import Credential

# Create your models here.
class User(models.Model):
    credential = models.ForeignKey(Credential, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    avatar = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    pronoun = models.CharField(max_length=20)
    description = models.TextField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Link(models.Model):
    credential = models.ForeignKey(Credential, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    url = models.URLField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Experience(models.Model):
    credential = models.ForeignKey(Credential, on_delete=models.CASCADE)
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    period = models.CharField(max_length=50)
    description = models.TextField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Education(models.Model):
    credential = models.ForeignKey(Credential, on_delete=models.CASCADE)
    institution = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    period = models.CharField(max_length=50)
    description = models.TextField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Skill(models.Model):
    credential = models.ForeignKey(Credential, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Graphic(models.Model):
    credential = models.ForeignKey(Credential, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    percentage = models.FloatField()
    color = models.CharField(max_length=7)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Topic(models.Model):
    credential = models.ForeignKey(Credential, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    topics = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
