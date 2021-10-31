from django.contrib.auth import login, logout,authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from ..form import StudentSignUpForm, TutorSignUpForm, UpdateStudentForm, UpdateStudentForm
from ..models import User, Course, Student, Tutor



class student_register(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = '../templates/users/student_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

def CourseListView(request):
    courselist = []
    for c in Course.objects.all():
        if request.user not in c.students.all():
            courselist.append(c) 
    return render(request, "../templates/students/home.html", {
        "courses": Course.objects.all() ,
        "courselist": courselist
    })
        

def CourseDetailView(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, "../templates/students/course_detail.html",{
        "object": course,
        "students": course.students.all(),

    })


class TutorDetailView(DetailView):
    model = Tutor
    template_name = '../templates/students/tutor_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def BookCourse(request, course_id ):
    if not request.user.is_authenticated:
        messages.warning(request, "Please Login")
        return HttpResponseRedirect(reverse("login"))

    course = get_object_or_404(Course, pk=course_id)
    if request.user not in course.students.all():
        course.students.add(request.user)
        course = Course.objects.get(id = course_id)
        course.count += 1
        course.save()
    return HttpResponseRedirect(reverse("course_detail", args=(course_id,)))
    
def CourseCancel(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.user in course.students.all():
        course.students.remove(request.user)
        course = Course.objects.get(id = course_id)
        course.count -= 1
        course.save()
    return HttpResponseRedirect(reverse("s_profile"))    
    
    

    
def ProfileView(request):
    courselist = []
    profile = request
    for p in Student.objects.all():
        if request.user.id == p.user.id:
            profile = p
    
    for c in Course.objects.all():
        if request.user in c.students.all():
            courselist.append(c) 
    return render(request, "../templates/students/profile.html", { "courselist": courselist, "profile" : profile })



def StudentUpdate(request):
    if request.method == 'POST':
        user_form = UpdateStudentForm(request.POST, instance=request.user)
        if user_form.is_valid:
            user_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('s_profile')
    else:
        user_form = UpdateStudentForm(instance=request.user)

    return render(request, '../templates/students/profile_update.html', {'u_form': user_form})