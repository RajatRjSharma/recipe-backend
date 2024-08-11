from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from .models import Recipe, RecipeLike
from .serializers import RecipeLikeSerializer, RecipeSerializer
from .permissions import IsAuthorOrReadOnly

import logging

logger = logging.getLogger(__name__)

class RecipeListAPIView(generics.ListAPIView):
    """
    Get: a collection of recipes
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (AllowAny,)
    filterset_fields = ('category__name', 'author__username')
    
    def get(self, request, *args, **kwargs):
        try:
            logger.info('Fetching list of recipes.')
            response = super().get(request, *args, **kwargs)
            logger.info('Successfully fetched list of recipes.')
            return response
        except Exception as e:
            logger.error(f'Error during fetching list of recipes: {e}', exc_info=True)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RecipeCreateAPIView(generics.CreateAPIView):
    """
    Create: a recipe
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        logger.info(f'Creating a recipe for user {self.request.user}.')
        serializer.save(author=self.request.user)
        logger.info('Recipe created successfully.')


class RecipeAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Get, Update, Delete a recipe
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    
    def get(self, request, *args, **kwargs):
        logger.info(f'Fetching details for recipe ID {self.kwargs["pk"]}.')
        response = super().get(request, *args, **kwargs)
        logger.info(f'Successfully fetched details for recipe ID {self.kwargs["pk"]}.')
        return response

    def put(self, request, *args, **kwargs):
        logger.info(f'Updating recipe ID {self.kwargs["pk"]}.')
        response = super().put(request, *args, **kwargs)
        logger.info(f'Successfully updated recipe ID {self.kwargs["pk"]}.')
        return response

    def delete(self, request, *args, **kwargs):
        logger.info(f'Deleting recipe ID {self.kwargs["pk"]}.')
        response = super().delete(request, *args, **kwargs)
        logger.info(f'Successfully deleted recipe ID {self.kwargs["pk"]}.')
        return response


class RecipeLikeAPIView(generics.CreateAPIView):
    """
    Like, Dislike a recipe
    """
    serializer_class = RecipeLikeSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        try:
            recipe = get_object_or_404(Recipe, id=self.kwargs['pk'])
            logger.info(f'User {request.user} likes recipe ID {recipe.id}.')
            new_like, created = RecipeLike.objects.get_or_create(
                user=request.user, recipe=recipe)
            if created:
                logger.info(f'New like created for recipe ID {recipe.id}.')
                new_like.save()
                return Response(status=status.HTTP_201_CREATED)
            logger.info(f'Recipe ID {recipe.id} already liked by user {request.user}.')
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Error during creating like for recipe ID {recipe.id}: {e}', exc_info=True)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            recipe = get_object_or_404(Recipe, id=self.kwargs['pk'])
            logger.info(f'User {request.user} unlikes recipe ID {recipe.id}.')
            like = RecipeLike.objects.filter(user=request.user, recipe=recipe)
            if like.exists():
                like.delete()
                logger.info(f'Removed like for recipe ID {recipe.id}.')
                return Response(status=status.HTTP_200_OK)
            logger.info(f'No like found for recipe ID {recipe.id} by user {request.user}.')
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Error during removing like for recipe ID {recipe.id}: {e}', exc_info=True)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
