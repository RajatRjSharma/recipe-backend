from django.urls import path

from recipe import views

app_name = "recipe"

urlpatterns = [
    path("", views.RecipeViewSet.as_view({"get": "list"}), name="recipe-list"),
    path(
        "<int:pk>/",
        views.RecipeViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="recipe-detail",
    ),
    path(
        "create/", views.RecipeViewSet.as_view({"post": "create"}), name="recipe-create"
    ),
    path("<int:pk>/like/", views.RecipeLikeAPIView.as_view(), name="recipe-like"),
]
