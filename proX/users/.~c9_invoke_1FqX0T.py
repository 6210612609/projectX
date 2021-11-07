from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
# Create your tests here.

from .models import User, Student, Tutor, Course

class CourseTestCase(TestCase):
    
    def setUp(self):
        
        user1 = User.objects.create(username='user1', password = make_password('1234'),email='user1@example.com')
        #student1 = Student.objects.create(user=user1)
        #user2 = User.objects.create(username='user2', password = make_password('1234'),email='user2@example.com')
        #tutor1 = Student.objects.create(user=user2)
        
    def test_student_login_view_with_authentication(self):
        c = Client()
        user = User.objects.get(username='user1',password = '1234')
        c.force_login(user)
        response = c.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
    
    def test_student_login_view_without_authentication(self):
        c = Client()
        user = User.objects.get(username='user1',password = '')
        response = c.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
    
    def test_tutor_login_view_with_authentication(self):
        c = Client()
        user = User.objects.get(username='user1',password = '1234')
        c.force_login(user)
        response = c.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
    
    def test_tutor_login_view_without_authentication(self):
        c = Client()
        user = User.objects.get(username='user2',password = '')
        response = c.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
