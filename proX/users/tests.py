from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

from .models import  *
from .form import *
from .views.main import *
from .views.students import UpdateStudentForm
from .views.tutors import CourseCreateView

class UserViewTestCase(TestCase):

    def setUp(self):
        User.objects.create(username='admin',first_name='first',last_name='last', password = make_password('1234'), email='admin@example.com', is_superuser = True)
        User.objects.create(username='student1',first_name='first',last_name='last', password = make_password('1234'), email='user@example.com', is_student = True)
        User.objects.create(username='tutor1',first_name='first',last_name='last', password = make_password('1234'), email='user@example.com', is_tutor = True)
        Course.objects.create(owner = User.objects.get(username='tutor1'), name = 'course1', detail = 'detail1')
    

    #logout view
    def test_logout_view(self):
        c = Client()
        responses = c.get(reverse('logout'))
        self.assertEqual(responses.status_code, 302)
        
    #Test Login
    def test_login_view(self):
        c = Client()
        responses = c.get(reverse('login'))
        self.assertEqual(responses.status_code, 200)
        
    #Test Tutor Login
    def test_tutor_login_success(self):
        c = Client()
        response = c.post(reverse('login'), {'username': 'tutor1','password': '1234'})
        self.assertEqual(response.status_code, 302)

    def test_tutor_login_failed(self):
        c = Client()
        response = c.post(reverse('login'), {'username': 'tutor1','password': '12356'})
        self.assertEqual(response.status_code, 200)


    #Register
    def test_register_view_view(self):
        c = Client()
        responses = c.get(reverse('register'))
        self.assertEqual(responses.status_code, 200)

    #Tutor SignUp
    def test_tutor_register_view_no_post(self):
        c = Client()
        responses = c.get(reverse('tutor_register'))
        self.assertEqual(responses.status_code, 200)

    def test_tutor_form_save_POST(self):
        user = User.objects.get(username='tutor1')
        form_data = {
            'username': 'user2',
            'password1': 'TestPassword1',
            'password2': 'TestPassword1',
            'first_name': 'user2f',
            'last_name': 'user2l',
            'nick_Name': 'user2n',
            'age': '12',
            'profile': 'user2_profile'
        }
        form = TutorSignUpForm(data=form_data)
        if(form.is_valid):
            tutor = Tutor.objects.create(user=user)
            tutor.save()
            form.save()
        c = Client()
        c.force_login(user)
        responses = c.get(reverse('index'))
        self.assertEqual(responses.status_code, 302)

    #TEST INDEX
    def test_index_without_audenticate(self):
        c = Client()
        response = c.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
   
    #TEST REGISTER USER
    #Student SignUp
    def test_student_register_view_no_post(self):
        c = Client()
        responses = c.get(reverse('student_register'))
        self.assertEqual(responses.status_code, 200)

    #Test Register for Student
    def test_register_student_form_save_POST(self):
        user = User.objects.get(username='student1')
        form_data = {
            'username': 'user3',
            'password1': 'TestPassword1',
            'password2': 'TestPassword1',
            'first_name': 'user3f',
            'last_name': 'user3l',
            'nick_Name': 'user3n',
            'age': '12',
            'degree': 'user3_degree'
        }
        c = Client()
        c.force_login(user)
        responses = c.post(reverse('student_register'), form_data)
        self.assertEqual(responses.status_code, 302)

    #Student SignUp Form
    def test_student_form_save_POST(self):
        user = User.objects.get(username='student1')
        form_data = {
            'username': 'user3',
            'password1': 'TestPassword1',
            'password2': 'TestPassword1',
            'first_name': 'user3f',
            'last_name': 'user3l',
            'nick_Name': 'user3n',
            'age': '12',
            'degree': 'user3_degree'
        }
        form = StudentSignUpForm(data=form_data)
        if(form.is_valid):
            student = Student.objects.create(user=user)
            student.save()
            form.save()
        self.assertTrue(form.is_valid())
        c = Client()
        c.force_login(user)
        responses = c.get(reverse('index'))
        self.assertEqual(responses.status_code, 302)
    
    #Tutor SignUp Form
    def test_register_tutor_form_save_POST(self):
        user = User.objects.get(username='tutor1')
        form_data = {
            'username': 'user3',
            'password1': 'TestPassword1',
            'password2': 'TestPassword1',
            'first_name': 'user3f',
            'last_name': 'user3l',
            'nick_Name': 'user3n',
            'age': '12',
            'profile': 'user3_degree'
        }
        c = Client()
        c.force_login(user)
        responses = c.post(reverse('index'), form_data)
        self.assertEqual(responses.status_code, 302)


   
    
        
class StudentViewTestCase(TestCase):

    def setUp(self):
        User.objects.create(username='admin',first_name='first',last_name='last', password = make_password('1234'), email='admin@example.com', is_superuser = True)
        User.objects.create(username='student1',first_name='first',last_name='last', password = make_password('1234'), email='user@example.com', is_student = True)
        User.objects.create(username='tutor1',first_name='first',last_name='last', password = make_password('1234'), email='user@example.com', is_tutor = True)
        Course.objects.create(owner = User.objects.get(username='tutor1'), name = 'course1', detail = 'detail1')
    
    #TEST STUDENT
    #index student    
    def test_student_index_view_with_authentication(self):
        c = Client()
        user = User.objects.get(username='student1')
        c1 = Course.objects.first()
        c1.save()
        c.force_login(user)
        c.get(reverse('course_detail', args=(c1.id,)))
        response = c.get(reverse('s_home'))
        self.assertEqual(response.status_code, 200)

    def test_student_index_view_without_authentication(self):
        c = Client()
        user = User.objects.get(username='student1')
        response = c.get(reverse('s_home'))
        self.assertEqual(response.status_code, 200)
        
    #Student Profile
    def test_student_profile(self):
        c = Client()
        user = User.objects.get(username='student1')
        c1 = Course.objects.first()
        c1.save()
        c.force_login(user)
        response1 = c.get(reverse('course_detail', args=(c1.id,)))
        response = c.get(reverse('s_profile'))
        self.assertEqual(response.status_code, 200)

    #Course Detail
    def test_course_detail(self):
        c = Client()
        user = User.objects.get(username='student1')
        c1 = Course.objects.first()
        c1.save()
        c.force_login(user)
        response = c.get(reverse('course_detail', args=(c1.id,)))
        self.assertEqual(response.status_code, 200)

    #Test Student Profile View
    def test_student_profile_view_without_authentication(self):
        c = Client()
        response = c.get(reverse('s_profile'))
        self.assertEqual(response.status_code, 302)
        
    
    #Test Student Update Form Valid
    def test_student_update_valid(self):
        user = User.objects.get(username='student1')
        c = Client()
        c.force_login(user)
        response1 = c.get(reverse('s_profile_update'))
        form_data = {
            'first_name': 'user2f',
            'last_name': 'user2l',
            'nick_Name': 'user2n',
            'age': '12',
            'degree': 'user2_degree'
        }
        form = UpdateStudentForm(data=form_data)
        if(form.is_valid):
            form.save()
        self.assertTrue(form.is_valid())

    #Student Profile View
    def test_student_profile_view_with_authentication(self):
        c = Client()
        user = User.objects.get(username='student1')
        c1 = Course.objects.first()
        c1.save()

        c.force_login(user)
        response1 = c.get(reverse('book_course', args=(c1.id,)))
        self.assertEqual(c1.students.count(), 1)
        response = c.get(reverse('s_profile'))
        self.assertEqual(response.status_code, 200)

    #Tset Student Update Profile Success
    def test_student_update_success(self):
        c = Client()
        user = User.objects.get(username='student1')
        c.force_login(user)
        form_data = {
            'first_name': 'user2f',
            'last_name': 'user2l',
            'nick_Name': 'user2n',
            'age': '12',
            'degree': 'user2_degree'
        }
        response = c.post(reverse('s_profile_update'), form_data)
        self.assertEqual(response.status_code, 302)

    #Test Student INDEX
    def test_student_index_view(self):
        c = Client()
        user = User.objects.get(username='student1')
        c.force_login(user)
        responses = c.get(reverse('index'))
        self.assertEqual(responses.status_code, 302)
    
    #Student Book Course
    def test_book_with_authentication(self):
        user = User.objects.get(username='student1')
        c1 = Course.objects.first()
        c1.save()

        c = Client()
        c.force_login(user)
        c.get(reverse('book_course', args=(c1.id,)))
        self.assertEqual(c1.students.count(), 1)
    
    def test_book_without_authentication(self):
        c1 = Course.objects.first()
        c1.save()

        c = Client()
        c.get(reverse('book_course', args=(c1.id,)))
        self.assertEqual(c1.students.count(), 0)

    #Test Cancel Booking
    def test_cancel_with_authentication(self):
        user = User.objects.get(username='student1')
        c1 = Course.objects.first()
        c1.save()

        c = Client()
        c.force_login(user)
        response1 = c.get(reverse('book_course', args=(c1.id,)))
        self.assertEqual(c1.students.count(), 1)
        response1 = c.get(reverse('course_cancel', args=(c1.id,)))
        self.assertEqual(c1.students.count(), 0)
    
   

class TutorViewTestCase(TestCase):
    
    def setUp(self):
        User.objects.create(username='admin',first_name='first',last_name='last', password = make_password('1234'), email='admin@example.com', is_superuser = True)
        User.objects.create(username='student1',first_name='first',last_name='last', password = make_password('1234'), email='user@example.com', is_student = True)
        User.objects.create(username='tutor1',first_name='first',last_name='last', password = make_password('1234'), email='user@example.com', is_tutor = True)
        Course.objects.create(owner = User.objects.get(username='tutor1'), name = 'course1', detail = 'detail1')
    
    #TEST TUTOR
    #index tutor   
    def test_tutor_index_view_with_authentication(self):
        c = Client()
        user = User.objects.get(username='tutor1')
        c.force_login(user)
        responses = c.get(reverse('index'))
        self.assertEqual(responses.status_code, 302)


    #Tutor Update Profile Success
    def test_tutor_update_profile_success(self):
        c = Client()
        user = User.objects.get(username='tutor1')
        c.force_login(user)
        form_data = {
            'first_name': 'user2f',
            'last_name': 'user2l',
            'nick_Name': 'user2n',
            'age': '12',
            'profile': 'user2_degree'
        }
        response = c.post(reverse('t_profile_update'), form_data)
        self.assertEqual(response.status_code, 302)

    #Tutor Update Profile View
    def test_tutor_update_valid(self):
        user = User.objects.get(username='tutor1')
        c = Client()
        c.force_login(user)
        response1 = c.get(reverse('t_profile_update'))
        form_data = {
            'first_name': 'user2f',
            'last_name': 'user2l',
            'nick_Name': 'user2n',
            'age': '12',
            'profile': 'user2_degree'
        }
        form = UpdateTutorForm(data=form_data)
        if(form.is_valid):
            form.save()
        self.assertTrue(form.is_valid())
    
    #Test Make Course 
    def test_make_course_form_save_POST(self):
        user = User.objects.get(username='tutor1')
        form_data = {
            'name': 'user3',
            'detail': 'detail23',
            'amount': '4',
            'price': '300'
        }
        c = Client()
        c.force_login(user)
        responses = c.post(reverse('make_course'), form_data)
        self.assertEqual(responses.status_code, 302)
    
    #Test Tutor CourseView 
    def test_tutor_view_with_comment(self):
        c = Client()
        Tutor.objects.create(user = User.objects.get(username='tutor1'))
        Review.objects.create(tutor = Tutor.objects.first(), student = User.objects.get(username='student1'), comment = 'comment1')
        user = User.objects.get(username='student1')
        tutor = User.objects.get(username='tutor1')
        c.force_login(user)
        response = c.get(reverse('tutor_detail', args=(tutor.id,)))
        self.assertEqual(response.status_code, 200)


    def test_tutor_view_without_comment(self):
        c = Client()
        Tutor.objects.create(user = User.objects.get(username='tutor1'))
        user = User.objects.get(username='student1')
        tutor = User.objects.get(username='tutor1')
        c.force_login(user)
        response = c.get(reverse('tutor_detail', args=(tutor.id,)))
        self.assertEqual(response.status_code, 200)
    
    def test_tutor_view_without_auth(self):
        c = Client()
        tutor = User.objects.get(username='tutor1')
        response = c.get(reverse('tutor_detail', args=(tutor.id,)))
        self.assertEqual(response.status_code, 302)
    
    #Test Tutor Profile
    def test_tutor_profile_view_without_authentication(self):
        c = Client()
        response = c.get(reverse('t_profile'))
        self.assertEqual(response.status_code, 302)

    def test_tutor_profile_view_with_authentication_with_review(self):
        c = Client()
        Tutor.objects.create(user = User.objects.get(username='tutor1'))

        Review.objects.create(tutor = Tutor.objects.first(), student = User.objects.get(username='student1'), comment = 'comment1')
        user = User.objects.get(username='tutor1')

        c.force_login(user)
        response = c.get(reverse('t_profile'))
        self.assertEqual(response.status_code, 200)
    
    def test_tutor_profile_view_with_authentication(self):
        c = Client()
        user = User.objects.get(username='tutor1')

        c.force_login(user)
        response = c.get(reverse('t_profile'))
        self.assertEqual(response.status_code, 200)
    
    def test_tutor_view_student(self):
        c = Client()
        user = User.objects.get(username='tutor1')
        c.force_login(user)
        response = c.get(reverse('student_detail'))
        self.assertEqual(response.status_code, 200)
        

    def test_tutor_view_student(self):
        c = Client()
        user = User.objects.get(username='tutor1')
        c.force_login(user)
        student = Student.objects.create(user = User.objects.get(username='student1'))
        response = c.get(reverse('student_detail', args=(student.pk,)))
        self.assertEqual(response.status_code, 200)    

    def test_tutor_view_student_without_auth(self):
        c = Client()
        student = Student.objects.create(user = User.objects.get(username='student1'))
        response = c.get(reverse('student_detail', args=(student.pk,)))
        self.assertEqual(response.status_code, 302)

    def test_course_detail(self):
        c = Client()
        user = User.objects.get(username='tutor1')
        c.force_login(user)
        course = Course.objects.create(owner = User.objects.get(username='tutor1'), name = 'course1', detail = 'detail1')
        response = c.get(reverse('t_course_detail', args=(course.pk,)))
        self.assertEqual(response.status_code, 200)

    def test_course_delete(self):
        c = Client()
        user = User.objects.get(username='tutor1')
        c.force_login(user)
        course = Course.objects.create(owner = User.objects.get(username='tutor1'), name = 'course1', detail = 'detail1')
        response = c.get(reverse('course_delete', args=(course.pk,)))
        self.assertEqual(response.status_code, 200)

class AdminViewTestCase(TestCase):

    def setUp(self):
        User.objects.create(username='admin',first_name='first',last_name='last', password = make_password('1234'), email='admin@example.com', is_superuser = True)
        User.objects.create(username='student1',first_name='first',last_name='last', password = make_password('1234'), email='user@example.com', is_student = True)
        User.objects.create(username='tutor1',first_name='first',last_name='last', password = make_password('1234'), email='user@example.com', is_tutor = True)
        Course.objects.create(owner = User.objects.get(username='tutor1'), name = 'course1', detail = 'detail1')
    
     #TEST ADMIN
    #Admin Index
    def test_admin_index_with_authendicated(self):
        c = Client()
        user = User.objects.get(username='admin')
        c.force_login(user)
        response = c.get(reverse('index'))
        self.assertEqual(response.status_code, 302)

    def test_admin_index_without_authendicated(self):
        c = Client()
        response = c.get(reverse('a_home'))
        self.assertEqual(response.status_code, 200)

    def test_admin_view_with_comment(self):
        c = Client()
        Tutor.objects.create(user = User.objects.get(username='tutor1'))
        Review.objects.create(tutor = Tutor.objects.first(), student = User.objects.get(username='student1'), comment = 'comment1')
        user = User.objects.get(username='admin')
        tutor = User.objects.get(username='tutor1')
        c.force_login(user)
        response = c.get(reverse('list_comment', args=(tutor.id,)))
        self.assertEqual(response.status_code, 200)


    def test_admin_view_without_comment(self):
        c = Client()
        Tutor.objects.create(user = User.objects.get(username='tutor1'))
        user = User.objects.get(username='admin')
        tutor = User.objects.get(username='tutor1')
        c.force_login(user)
        response = c.get(reverse('list_comment', args=(tutor.id,)))
        self.assertEqual(response.status_code, 200)

    def test_admin_delete_comment(self):
        c = Client()
        Tutor.objects.create(user = User.objects.get(username='tutor1'))
        review = Review.objects.create(tutor = Tutor.objects.first(), student = User.objects.get(username='student1'), comment = 'comment1')
        user = User.objects.get(username='admin')
        tutor = User.objects.get(username='tutor1')
        c.force_login(user)
        response = c.post(reverse('delete_review', args=(tutor.id, review.id)))
        self.assertEqual(response.status_code, 302)
    

    