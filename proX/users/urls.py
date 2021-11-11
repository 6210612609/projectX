from django.urls import path
from .views  import main, students, tutors

urlpatterns=[

     path('',main.index, name='index'),
     path('admins/', main.TutorListView, name='a_home'),
     path('admins/tutor/<int:tutor_id>', main.CommentListView, name='list_comment'),
     path('admins/tutor/<int:tutor_id>/<int:review_id>/delete', main.ReviewDelete, name='delete_review'),
     
     

     path('students/', students.CourseListView, name='s_home'),
     path('students/profile/', students.ProfileView, name='s_profile'),
     path('students/profile/update', students.StudentUpdate, name='s_profile_update'),
     path('students/course/<int:course_id>', students.CourseDetailView, name='course_detail'),
     path('students/course/<int:course_id>/cancel', students.CourseCancel, name='course_cancel'),
     path('students/course/<int:course_id>/book', students.BookCourse, name='book_course'),
     path('students/course/tutor/<int:tutor_id>', students.TutorDetailView, name='tutor_detail'),
     
     
     path('students/course/tutor/<int:tutor_id>/comment', students.add_reviews, name='tutor_comment'),


     path('tutors/', tutors.CourseListView.as_view(), name='t_home'),
     path('tutors/profile', tutors.ProfileView, name='t_profile'),
     path('tutors/profile/update', tutors.TutorUpdate, name='t_profile_update'),
     path('tutors/course/make_course/',tutors.CourseCreateView.as_view(), name='make_course'),
     path('tutors/course/<int:course_id>/',tutors.CourseDetailView, name='t_course_detail'),
     path('tutors/course/<int:pk>/update', tutors.CourseUpdateView.as_view(), name='course_update'),
     path('tutors/course/<int:pk>/delete', tutors.CourseDeleteView.as_view(), name='course_delete'),
     path('tutors/student/<int:student_id>/', tutors.studentDetailView, name='student_detail'),

    




]