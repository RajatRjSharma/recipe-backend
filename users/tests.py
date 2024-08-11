from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from recipe.models import Recipe, RecipeCategory
from .models import Profile

User = get_user_model()

class UserRegistrationTests(APITestCase):
    
    def test_user_registration_success(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'strongpassword123'
        }
        response = self.client.post(reverse('users:create-user'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'testuser@example.com')

    def test_user_registration_missing_password(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com'
        }
        response = self.client.post(reverse('users:create-user'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_user_registration_invalid_email(self):
        data = {
            'username': 'testuser',
            'email': 'notanemail',
            'password': 'strongpassword123'
        }
        response = self.client.post(reverse('users:create-user'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        
        
        
class UserLoginTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='strongpassword123'
        )

    def test_user_login_success(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'strongpassword123'
        }
        response = self.client.post(reverse('users:login-user'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)

    def test_user_login_invalid_credentials(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('users:login-user'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)





class UserLogoutTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='strongpassword123'
        )
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token.access_token))

    def test_user_logout_success(self):
        data = {'refresh': str(self.token)}
        response = self.client.post(reverse('users:logout-user'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_user_logout_invalid_token(self):
        data = {'refresh': 'invalidtoken'}
        response = self.client.post(reverse('users:logout-user'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserInformationTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='strongpassword123'
        )
        self.client.force_authenticate(user=self.user)

    def test_get_user_info_success(self):
        response = self.client.get(reverse('users:user-info'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'testuser@example.com')

    def test_update_user_info_success(self):
        data = {'username': 'newusername'}
        response = self.client.patch(reverse('users:user-info'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'newusername')

    def test_update_user_info_unauthenticated(self):
        self.client.logout()
        data = {'username': 'newusername'}
        response = self.client.patch(reverse('users:user-info'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserProfileTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='strongpassword123'
        )
        self.profile, _ = Profile.objects.get_or_create(user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_get_user_profile_success(self):
        response = self.client.get(reverse('users:user-profile'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_profile_success(self):
        data = {'bio': 'Updated bio'}
        response = self.client.patch(reverse('users:user-profile'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bio'], 'Updated bio')


class UserBookmarkTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='strongpassword123'
        )
        self.profile, _ = Profile.objects.get_or_create(user=self.user)
        self.category = RecipeCategory.objects.create(name="Desserts")
        self.recipe = Recipe.objects.create(
            author=self.user,
            category=self.category,
            title="Chocolate Cake",
            desc="Delicious chocolate cake",
            cook_time="01:00:00",
            ingredients="Flour, Sugar, Cocoa",
            procedure="Mix ingredients and bake",
        )
        self.client.force_authenticate(user=self.user)

    def test_add_bookmark_success(self):
        response = self.client.post(reverse('users:user-bookmark', kwargs={'pk': self.user.id}), {'id': self.recipe.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.recipe, self.profile.bookmarks.all())

    def test_remove_bookmark_success(self):
        self.profile.bookmarks.add(self.recipe)
        response = self.client.delete(reverse('users:user-bookmark', kwargs={'pk': self.user.id}), {'id': self.recipe.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.recipe, self.profile.bookmarks.all())


class PasswordChangeTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='strongpassword123'
        )
        self.client.force_authenticate(user=self.user)

    def test_password_change_success(self):
        data = {
            'old_password': 'strongpassword123',
            'new_password': 'newstrongpassword456'
        }
        response = self.client.patch(reverse('users:change-password'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newstrongpassword456'))

    def test_password_change_wrong_old_password(self):
        data = {
            'old_password': 'wrongpassword',
            'new_password': 'newstrongpassword456'
        }
        response = self.client.patch(reverse('users:change-password'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('old_password', response.data)
