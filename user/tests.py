from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from .forms import *

User = get_user_model()

REGISTER_USER_URL = reverse('user:register_view')
VERIFY_USER_URL = reverse("user:verification_view")
FORGET_PASSWORD_URL = reverse("user:forget_password")

class UserTest(TestCase):

    def setUp(self):
        self.client = Client()
        
        primary = {
            'email': 'lordofhell@email.com',
            'phone': '09226996206',
            'password1': 'pandoras.0',
        }
        timer = timezone.now() - timezone.timedelta(minutes=2)
        form = RegisterForm(primary, timer=timer)
        self.assertTrue(form.is_valid())
        form.save()
        self.client.force_login(form.instance)


        return super().setUp()

    def test_create_user(self):
        
        user_input = {
            'email': 'ahmad@email.com',
            'phone': '09226996209',
            'password1': 'pandoras.0',
        }
        timer = timezone.now() - timezone.timedelta(minutes=2)
        form = RegisterForm(user_input, timer=timer)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.instance.email, user_input.get('email'))
        response = self.client.post(REGISTER_USER_URL, user_input, follow=True)
        self.assertEqual(response.status_code, 200)
        # self.assertTrue(form.instance.check_password(user_input.get("password1")))

    def test_create_user_fail(self):
        user_input = {
            'email': 'huskar_assassin@yahoo.com', # not unique
            'phone': '09226996207', # not unique
            'password1': 'pandor', # less than 8 character
        }
        form = RegisterForm(user_input, timer=timezone.now())
        self.assertFalse(form.is_valid())
        response = self.client.post(REGISTER_USER_URL, user_input)
        self.assertEqual(response.status_code, 302)
        # get_response = self.client.get(REGISTER_USER_URL)
        # password_error = form.errors.get('password1')
        # self.assertFormError(response, 'register_form', 'password1', password_error)
        # email_error = form.errors.get('email')
        # self.assertFormError(response, 'register_form', 'email', email_error)
        # phone_error = form.errors.get('phone')
        # self.assertFormError(response, 'register_form', 'phone', phone_error)
    
    def test_user_exists(self):
        user_input = {
            'email': 'lordofhell@email.com',
            'phone': '09226996206',
            # 'password': 'pandoras.0',
        }
        user = User.objects.filter(**user_input)
        self.assertTrue(user.exists())
        response = self.client.post(REGISTER_USER_URL, user_input)
        self.assertEqual(response.status_code, 302)


    def test_verification(self):
        get_response = self.client.get(VERIFY_USER_URL)
        self.assertEqual(get_response.status_code, 302) # without session

        timer = timezone.now() + timezone.timedelta(minutes=2)
        session = self.client.session
        session['sms_validate'] = 123454
        session['register_timer'] = str(timer)
        session.save()

        get_response2 = self.client.get(VERIFY_USER_URL)
        self.assertEqual(get_response2.status_code, 200) # with session

        verify_form = VerificationForm({"code": '123454'}, session=session, expire_time=timer)
        self.assertTrue(verify_form.is_valid())

    def test_forget_password(self):
        form_data = {'email': 'lordofhell@email.com'}
        form = ForgetPasswordForm(form_data)
        self.assertTrue(form.is_valid())

    def test_forget_password_fail(self):
        form_data = {'email': 'lordofhell226@gmail.com'} # email does not exists
        form = ForgetPasswordForm(form_data)
        self.assertFalse(form.is_valid())