import datetime
from django.db import models
import re
# Create your models here.

class UserManager(models.Manager):
    def validateregistry(self,postdata):
        errors={}
        if len(postdata["first_name"])<2:
            errors['first_name']="first name needs to be larger than 2 characters"
        if len(postdata["last_name"])<2:
            errors['last_name']="last name needs to be larger than 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postdata['email']):    # test whether a field matches the pattern            
            errors['email_invalid'] = "Invalid email address!"
        if User.objects.filter(email=postdata['email']).exists():
            errors['email_used'] = "email already used!"
        if len(postdata['password'])<8:
            errors['password_length']="password too short!"
        if postdata['password']!=postdata['confirmpassword']:
            errors['confirm_password']="passwords do not match!"
        
        return errors
    

class ProjectManager(models.Manager):
    def validateproject(self,postdata):
        errors={}
        if len(postdata['name'])<3:
            errors['name']="name should be longer than 3"
        if len(postdata['description'])<10:
            errors['description']="description should be longer than 10"
        if not postdata['start_date'] or not postdata['end_date']:
            errors['date']="dates should not be blank"
        elif datetime.datetime.strptime(postdata['start_date'], "%Y-%m-%d").date() > datetime.date.today():
            errors['start_date'] = "start date should be in the past!"
        return errors

class User (models.Model):

    first_name =models.CharField(max_length=255)
    last_name =models.CharField(max_length=255)

    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=UserManager()


class Project (models.Model):
    name=models.CharField(max_length=255)
    owner = models.ForeignKey(User, related_name="owner", on_delete=models.CASCADE)
    members= models.ManyToManyField(User, related_name='members')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()
    objects=ProjectManager()