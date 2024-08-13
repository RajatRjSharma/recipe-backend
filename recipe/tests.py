from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from recipe.models import Recipe, RecipeCategory, RecipeLike

User = get_user_model()


class RecipeTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="strongpassword123",
        )
        self.client.force_authenticate(user=self.user)

        self.category = RecipeCategory.objects.create(name="Dessert")

        self.recipe = Recipe.objects.create(
            title="Test Recipe",
            desc="A description of the test recipe",
            cook_time="00:30:00",
            ingredients="Sugar, Flour",
            procedure="Mix and bake",
            author=self.user,
            category=self.category,
        )

    def test_list_recipes(self):
        response = self.client.get(reverse("recipe:recipe-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], self.recipe.title)

    def test_create_recipe_unauthenticated(self):
        self.client.logout()
        data = {
            "title": "New Recipe",
            "desc": "A description of the new recipe",
            "cook_time": "01:00:00",
            "ingredients": "Eggs, Milk",
            "procedure": "Mix and cook",
            "category": {"name": "Dessert"},
        }
        response = self.client.post(
            reverse("recipe:recipe-create"), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_recipe(self):
        response = self.client.get(
            reverse("recipe:recipe-detail", kwargs={"pk": self.recipe.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.recipe.title)

    def test_update_recipe_unauthenticated(self):
        self.client.logout()
        data = {
            "title": "Updated Recipe",
            "desc": "An updated description",
            "cook_time": "02:00:00",
            "ingredients": "Sugar, Milk",
            "procedure": "Mix and bake",
            "category": {"name": "Dessert"},
        }
        response = self.client.put(
            reverse("recipe:recipe-detail", kwargs={"pk": self.recipe.id}),
            data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_recipe_success(self):
        response = self.client.delete(
            reverse("recipe:recipe-detail", kwargs={"pk": self.recipe.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=self.recipe.id).exists())

    def test_delete_recipe_unauthenticated(self):
        self.client.logout()
        response = self.client.delete(
            reverse("recipe:recipe-detail", kwargs={"pk": self.recipe.id})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_like_recipe_success(self):
        response = self.client.post(
            reverse("recipe:recipe-like", kwargs={"pk": self.recipe.id})
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            RecipeLike.objects.filter(user=self.user, recipe=self.recipe).exists()
        )

    def test_like_recipe_unauthenticated(self):
        self.client.logout()
        response = self.client.post(
            reverse("recipe:recipe-like", kwargs={"pk": self.recipe.id})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unlike_recipe_success(self):
        # First, like the recipe
        self.client.post(reverse("recipe:recipe-like", kwargs={"pk": self.recipe.id}))
        # Then, unlike the recipe
        response = self.client.delete(
            reverse("recipe:recipe-like", kwargs={"pk": self.recipe.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            RecipeLike.objects.filter(user=self.user, recipe=self.recipe).exists()
        )

    def test_unlike_recipe_unauthenticated(self):
        # First, like the recipe
        self.client.post(reverse("recipe:recipe-like", kwargs={"pk": self.recipe.id}))
        self.client.logout()
        # Then, try to unlike the recipe
        response = self.client.delete(
            reverse("recipe:recipe-like", kwargs={"pk": self.recipe.id})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
