from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models

from unittest.mock import patch


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

    def test_ingredient_str(self):
        """Test the ingredient string rep"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(), name='Cucumber')

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test recipe string rep """
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='lasagna',
            time_minute=5,
            price=10.25)

        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        exp_path = f'upload/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
