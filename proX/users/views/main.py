from django.contrib.auth import login, logout,authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.views.generic import CreateView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse, reverse_lazy

from ..form import StudentSignUpForm, TutorSignUpForm
from ..models import User, Course, Tutor, Review

def register(request):
        return render(request, '../templates/users/register.html')

def login_request(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                login(request,user)
                return redirect('/')
            else:
                messages.error(request,"Invalid username or password")
        else:
                messages.error(request,"Invalid username or password")
    return render(request, '../templates/users/login.html',
    context={'form':AuthenticationForm()})

def logout_view(request):
    logout(request)
    return redirect('/')

    
def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
           return redirect('a_home')
        if request.user.is_tutor:
            return redirect('t_home')
        else:
            return redirect('s_home')
    else:        
        courselist = []
        availablecourse = []
        for i in Course.objects.all():
            if (i.count < i.amount):
                courselist.append(i)
        check_search = False
        search = ''
        
        if request.method == "POST":
            search = request.POST["search"]
            check_search = True
            for c in courselist:
                if c.search(search):
                    availablecourse.append(c)
        else:
            for c in courselist:
                availablecourse.append(c) 
        return render(request, "../templates/main/index.html", {
            "courselist": availablecourse,
            "check_search": check_search,
            "search" : search
        })
        
def TutorListView(request):
    tutor = Tutor.objects.all()
    return render(request, '../templates/admins/home.html', { "tutor" : tutor })

def CommentListView(request, tutor_id):
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
    return render(request, "../templates/admins/tutor_detail.html",{
        "object": tutor,
        "reviews": review,
        "avgstar": avgstar
    })

def ReviewDelete(request, tutor_id, review_id):
    Review.objects.filter(id=review_id).delete()
    return HttpResponseRedirect(reverse("list_comment", args=(tutor_id,)))

def about(request):
    return render(request, '../templates/main/about.html') 
    
