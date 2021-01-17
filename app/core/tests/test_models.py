from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='test@londondev.com', password='testpass'):
    """ Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """ Test creating a new user with an email is successful"""
        email = 'test@londondev.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """ test email is not case sensitive """
        email = 'test@LONDONAPPDEV.COM'
        user = get_user_model().objects.create_user(
            email=email, password='Test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_email_provided(self):
        """ make sure email is required """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, password='Test123')

    def test_superuser_created(self):
        """ test creating a new super user """
        user = get_user_model().objects.create_superuser(
            "test@londonapp.com",
            "Test1234"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(user=sample_user(), name='Vegan')

        self.assertEqual(str(tag), tag.name)
