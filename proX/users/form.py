from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import User,Student,Tutor,Course


class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    nick_Name = forms.CharField(required=True)
    age = forms.CharField(required=True)
    degree = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User


    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.nick_Name=self.cleaned_data.get('nick_Name')
        user.age=self.cleaned_data.get('age')
        user.degree=self.cleaned_data.get('degree')
        user.save()
        student = Student.objects.create(user=user)
        student.save()
        return user




class TutorSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    nick_Name = forms.CharField(required=True)
    age = forms.CharField(required=True)
    profile = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_tutor = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.nick_Name = self.cleaned_data.get('nick_Name')
        user.age = self.cleaned_data.get('age')
        user.profile = self.cleaned_data.get('profile')
        user.save()
        tutor = Tutor.objects.create(user=user)
        tutor.save()
        return user


class UpdateStudentForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    nick_Name = forms.CharField(required=True)
    age = forms.CharField(required=True)
    degree = forms.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'nick_Name', 'age', 'degree']
        
    

class UpdateTutorForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    nick_Name = forms.CharField(required=True)
    age = forms.CharField(required=True)
    profile = forms.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'nick_Name', 'age', 'profile']
        
