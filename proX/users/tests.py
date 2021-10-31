from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
# Create your tests here.

from .models import  *

class UserViewTestCase(TestCase):

    def setUp(self):
        User.objects.create(username='student1', password = make_password('1234'), email='user@example.com', is_student = True)
        User.objects.create(username='tutor1', password = make_password('1234'), email='user@example.com', is_tutor = True)
        Course.objects.create(owner = User.objects.get(username='tutor1'), name = 'course1', detail = 'detail1')
        
        
    def test_student_index_view_with_authentication(self):
        c = Client()
        user = User.objects.get(username='student1')
        c1 = Course.objects.first()
        c1.save()
        c.force_login(user)
        response1 = c.get(reverse('course_detail', args=(c1.id,)))        
        response2 = c.get(reverse('s_home'))
        self.assertEqual(response2.status_code, 200)
    
    def test_student_profile(self):
        c = Client()
        user = User.objects.get(username='student1')
        c1 = Course.objects.first()
        c1.save()
        c.force_login(user)
        response1 = c.get(reverse('course_detail', args=(c1.id,)))       
        response = c.get(reverse('s_profile'))
        self.assertEqual(response.status_code, 200)
        
    def test_course_detail(self):
        c = Client()
        user = User.objects.get(username='student1')
        c1 = Course.objects.first()
        c1.save()
        c.force_login(user)
        response = c.get(reverse('course_detail', args=(c1.id,)))
        self.assertEqual(response.status_code, 200)
    
    def test_student_index_view_without_authentication(self):
        c = Client()
        user = User.objects.get(username='student1')
        response = c.get(reverse('s_home'))
        self.assertEqual(response.status_code, 200)
    
    
    #Tutor Login
    def test_tutor_index_view_with_authentication(self):
        c = Client()
        user = User.objects.get(username='tutor1')
        c.force_login(user)
        response = c.get(reverse('t_home'))
        self.assertEqual(response.status_code, 200)
    
   # def test_tutor_index_view_without_authentication(self):
   #     c = Client()
   #     user = User.objects.get(username='tutor1')
   #     response = c.get(reverse('t_home'))
   #     self.assertEqual(response.status_code, 200)
    
    #def test_tutor_login_success(self):
    #    c = Client()
    #    user = User.objects.get(username='tutor1')
    #    response = c.post(reverse('login'), {{'username': 'tutor1','password': '1234'}})
    #    self.assertEqual(responses.status_code, 302)
    
    #def test_tutor_login_failed(self):
    #    c = Client()
    #    user = User.objects.get(username='tutor1')
   # #    response = c.post(reverse('login'), {{'username': 'tutor1','password': ''}})
       # self.assertEqual(responses.status_code, 302)
    
    #logout view
    def test_logout_view(self):
        c = Client()
        responses = c.get(reverse('logout'))
        self.assertEqual(responses.status_code, 302)

    
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
    
    #def test_register_view_duplicate_username(self):
    #    c = Client()
    #   responses = c.post(reverse('tutor'),
    #                      {'username': 'user1',
    #                        'password': '147852369',
    #                        're_password': '147852369',
    #                        'first_name': 'firstname',
    #                        'last_name': 'lastname',
    #                        'nick_Name': 'nickname',
    #                        'age': 'age',
    #                        'profile': 'my_profile'
    #                       })
    #    self.assertEqual(responses.status_code, 200)

    
    
    
