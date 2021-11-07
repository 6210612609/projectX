from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
# Create your tests here.

from .models import User, Student, Tutor, Course

class CourseTestCase(TestCase):
    
    def setUp(self):
        
        #user1 = User.objects.create(username='user1', password = make_password('1234'),email='user1@example.com')
        student1 = User.objects.create(username='student1', password = make_password('1234'),email='user1@example.com')
        #student1 = Student.objects.create(user=user1)
        #user2 = User.objects.create(username='user2', password = make_password('1234'),email='user2@example.com')
        #tutor1 = Student.objects.create(user=user2)
        course = Course.objects.create(name ='Physic',detail = 'No',amount ='5',count ='0' ,price ='1')
        
    def test_login_view_with_authentication(self):
        c = Client()
        user = User.objects.get(username='student1')
        c.force_login(user)
        response = c.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_view_without_authentication(self):
        c = Client()
        user = User.objects.get(username='student1')
        c.force_login(user)
        response = c.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
    
    
    
    def book_with_authenciation(self):
        c = Client()
        c1 = Course.objects.first()
        c1.save()
        user = User.objects.get(username='user1')
        if user not in c1.students.all():
            c1.student.add()
            count = Course.ojects.get(c1.id)
            count.nowquantity += 1
            count.save
        response = c.get(reverse('courses:book', args=(c1.id,)))
        self.assertEqual(response.status_code, 200)


class UserTestCase(TestCase):
    
    def setUp(self):

        en_password = make_password('1234')
        User.objects.create(username='user2', password=en_password, email='user2@exp.com', is_student='True')
        User.objects.create(username='admin', password=en_password, email='admin@exp.com', is_tutor='True')

    
    
    
    
    
    
    
