from django.contrib.auth import login, logout,authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from ..form import StudentSignUpForm, TutorSignUpForm, UpdateStudentForm, UpdateStudentForm
from ..models import User, Course, Student, Tutor, Review



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
    check_search = False
    search = ''
    if request.method == "POST":
        search = request.POST["search"]
        check_search = True
        for c in Course.objects.all():
            if c.search(search):
                courselist.append(c)
    else:
        for c in Course.objects.all():
            if request.user not in c.students.all():
                courselist.append(c) 
    return render(request, "../templates/students/home.html", {
        "courselist": courselist,
        "check_search": check_search,
        "search" : search
    })
        

def CourseDetailView(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, "../templates/students/course_detail.html",{
        "object": course,
        "students": course.students.all(),

    })

def TutorDetailView(request, tutor_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Please Login")
        return HttpResponseRedirect(reverse("login"))
    tutor = get_object_or_404(Tutor, pk=tutor_id)
    review = []
    for r in Review.objects.all():
        if r.tutor.user.id == tutor_id:
            review.append(r) 
    num = 0
    sumstar = 0
    for s in review:
        sumstar += s.star
        num += 1
    if (num == 0):
        avgstar = 0
    else:
        avgstar = sumstar/num
        avgstar = "{:.1f}".format(avgstar)
    return render(request, "../templates/students/tutor_detail.html",{
        "object": tutor,
        "reviews": review,
        "avgstar": avgstar
    })

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
    if not request.user.is_authenticated:
        messages.warning(request, "Please Login")
        return HttpResponseRedirect(reverse("login"))
    courselist = []
    profile = request
    for c in Course.objects.all():
        if request.user in c.students.all():
            courselist.append(c) 
    return render(request, "../templates/students/profile.html", { "courselist": courselist, "profile" : profile })



def StudentUpdate(request):
    if request.method == 'POST':
        user_form = UpdateStudentForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid:
            user_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('s_profile')
    else:
        user_form = UpdateStudentForm(instance=request.user)

    return render(request, '../templates/students/profile_update.html', {'u_form': user_form})
    

def add_reviews(request, tutor_id):
    if request.method == "POST":
        tutor = get_object_or_404(Tutor, pk=tutor_id)
        student = get_object_or_404(User, pk=request.user.id)
        comment = request.POST.get("comment")
        star = request.POST.get("star")
            
        review = Review(tutor = tutor,student=student, comment=comment, star=star)
        review.save()
        messages.success(request, "Thank You for Reviewing ^^")
    return HttpResponseRedirect(reverse("tutor_detail", args=(tutor_id,)))
    
