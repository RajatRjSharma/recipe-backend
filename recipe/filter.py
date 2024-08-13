from django_filters import rest_framework as filters
from .models import Recipe


class RecipeFilter(filters.FilterSet):
    category_name = filters.CharFilter(
        field_name="category__name", lookup_expr="icontains"
    )
    author_username = filters.CharFilter(
        field_name="author__username", lookup_expr="icontains"
    )

    class Meta:
        model = Recipe
        fields = ["category_name", "author_username"]
