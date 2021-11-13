from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_tutor = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nick_Name = models.CharField(max_length=20)
    age = models.CharField(max_length=16)
    degree = models.CharField(max_length=20, default = '-')
    profile = models.TextField(max_length=512, default = "-")
    profile_pic = models.ImageField(default = "profile2.png", null = True, blank =True)



class Student(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)



class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)



class Course(models.Model):
    owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'owners')
    name = models.CharField(max_length = 64)
    detail = models.CharField(max_length = 256)
    amount = models.IntegerField(default = 4)
    count = models.IntegerField(default = 0)
    price = models.IntegerField(default = 300)
    students = models.ManyToManyField(User, blank=True, related_name= "courses")

    def search(self, search):
        if search.lower() in self.name.lower():
            return True
        return False

class Review(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete = models.CASCADE)
    student = models.ForeignKey(User, on_delete = models.CASCADE)
    comment = models.TextField()
    posted_on = models.DateField(default=timezone.now)
    star = models.IntegerField(default = 0,)
    