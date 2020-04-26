from django.test import TestCase
from django.contrib.auth import get_user_model


class  ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email and is sucessful."""
        email = 'test@mztech.com'
        password='Testpassword123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_mormalized(self):
        """Test the email for a new user is mormalized"""
        email = 'test@MZTECH.COM'
        user = get_user_model().objects.create_user(email, 'test1234')

        self.assertEqual(user.email, email.lower())

    def test_new_invalid_email(self):
        """Test creating user with no email raise error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test1234')


    def test_create_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
        'test@mztech.com',
        'test1234'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)