from django.conf import settings
from django.db import models
from django.utils import timezone



class detail(models.Model):
    emp_id = models.IntegerField(unique=True)
    manager_id = models.IntegerField()
    status = models.CharField(max_length=10)
    last_name = models.CharField(max_length=40)
    preferred_name = models.CharField(max_length=40)
    work_phone = models.TextField()
    personal_email = models.CharField(max_length=50)
    location = models.TextField()
    department = models.CharField(max_length=50)
    manager = models.CharField(max_length=40,null=True)
    subordinates_url = models.TextField(null=True)

    def __unicode__(self):
        return self.post


    """location = models.TextField(default="null")
    subordinates = models.TextField(default="null")
    department = models.TextField(default="null")
    employments = models.TextField(default="null")"""
    
