from django.contrib import admin
from .models import User, Student, Tutor, Course, Review

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Tutor)
admin.site.register(Course)
admin.site.register(Review)