from django.urls import path
from .views  import main, students, tutors

urlpatterns=[

     path('',main.index, name='index'),

     path('students/', students.CourseListView, name='s_home'),
     path('students/profile/', students.ProfileView, name='s_profile'),
     path('students/profile/update', students.StudentUpdate, name='s_profile_update'),
     path('students/course/<int:course_id>', students.CourseDetailView, name='course_detail'),
     path('students/course/<int:course_id>/cancel', students.CourseCancel, name='course_cancel'),
     path('students/course/<int:course_id>/book', students.BookCourse, name='book_course'),
     path('students/course/tutor/<int:pk>', students.TutorDetailView.as_view(), name='tutor_detail'),




     path('tutors/', tutors.CourseListView.as_view(), name='t_home'),
     path('tutors/profile', tutors.ProfileView, name='t_profile'),
     path('tutors/profile/update', tutors.TutorUpdate, name='t_profile_update'),
     path('tutors/course/make_course/',tutors.CourseCreateView.as_view(), name='make_course'),
     path('tutors/course/<int:pk>/', tutors.CourseUpdateView.as_view(), name='course_update'),
     path('tutors/course/<int:pk>/delete', tutors.CourseDeleteView.as_view(), name='course_delete'),







]