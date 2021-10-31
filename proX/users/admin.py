from django.contrib import admin
from .models import User, Student, Tutor, Course

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Tutor)
admin.site.register(Course)