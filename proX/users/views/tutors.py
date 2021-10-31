from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from ..models import User, Course, Tutor
from ..form import StudentSignUpForm, TutorSignUpForm, UpdateTutorForm


class tutor_register(CreateView):
    model = User
    form_class = TutorSignUpForm
    template_name = '../templates/users/tutor_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


class CourseListView(ListView):
    model = Course
    ordering = ('name',)
    context_object_name = 'owners'
    template_name = '../templates/tutors/home.html'
    
    def get_queryset(self):
        queryset = self.request.user.owners\
            .select_related('owner')
        return queryset
    


class CourseCreateView(CreateView):
    model = Course
    fields = ('name', 'detail', 'amount','price')
    template_name = '../templates/tutors/make_course.html'

    def form_valid(self, form):
        course = form.save(commit=False)
        course.owner = self.request.user
        course.save()
        messages.success(self.request, 'Course added Success')
        return redirect('/tutors')


class CourseUpdateView(UpdateView):
    model = Course
    fields = ('name', 'detail', 'amount','price' )
    context_object_name = 'owners'
    template_name = '../templates/tutors/course_update_form.html'

    def get_queryset(self):
        
        return self.request.user.owners.all()

    def get_success_url(self):
        return reverse('course_update', kwargs={'pk': self.object.pk})


class CourseDeleteView(DeleteView):
    model = Course
    context_object_name = 'owners'
    template_name = '../templates/tutors/course_delete_confirm.html'
    success_url = reverse_lazy('t_home')

    def delete(self, request, *args, **kwargs):
        course = self.get_object()
        messages.success(request, 'The course %s was deleted with success!' % course.name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.owners.all()

def ProfileView(request):
    
    for p in Tutor.objects.all():
        if request.user.id == p.user.id:
            profile = p

    return render(request, "../templates/tutors/profile.html", { "tutor" : profile })
    
    
    
def TutorUpdate(request):
    if request.method == 'POST':
        user_form = UpdateTutorForm(request.POST, instance = request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('t_profile')
    else:
        user_form = UpdateTutorForm(instance=request.user)

    return render(request, '../templates/tutors/profile_update.html', {'form': user_form})    