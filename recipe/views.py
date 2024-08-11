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
            logger.debug('Enter get list of recipes')
            response = super().get(request, *args, **kwargs)
            logger.debug('Exit get list of recipes : success')
            return response
        except Exception as e:
            logger.error(f'Error get list of recipes: {e}', exc_info=True)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RecipeCreateAPIView(generics.CreateAPIView):
    """
    Create: a recipe
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RecipeAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Get, Update, Delete a recipe
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    
    def get(self, request, *args, **kwargs):
        try:
            logger.debug(f'Enter get recipe detail : {self.kwargs["pk"]}')
            response = super().get(request, *args, **kwargs)
            logger.debug(f'Exit get recipe detail : {self.kwargs["pk"]} : success')
            return response
        except Exception as e:
            logger.error(f'Error get recipe detail : {self.kwargs["pk"]} : {e}', exc_info=True)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def put(self, request, *args, **kwargs):
        try:
            logger.debug(f'Enter update recipe detail : {self.kwargs["pk"]}')
            response = super().put(request, *args, **kwargs)
            logger.debug(f'Exit update recipe detail : {self.kwargs["pk"]} : success')
            return response
        except Exception as e:
            logger.error(f'Error update recipe detail : {self.kwargs["pk"]} : {e}', exc_info=True)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        try:
            logger.debug(f'Enter delete recipe : {self.kwargs["pk"]}')
            response = super().delete(request, *args, **kwargs)
            logger.debug(f'Exit delete recipe : {self.kwargs["pk"]}: success')
            return response
        except Exception as e:
            logger.error(f'Error delete recipe : {self.kwargs["pk"]} : {e}', exc_info=True)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RecipeLikeAPIView(generics.CreateAPIView):
    """
    Like, Dislike a recipe
    """
    serializer_class = RecipeLikeSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        try:
            recipe = get_object_or_404(Recipe, id=self.kwargs['pk'])
            logger.debug(f'Enter like recipe : {request.user} {recipe.id}')
            new_like, created = RecipeLike.objects.get_or_create(
                user=request.user, recipe=recipe)
            if created:
                logger.debug(f'Exit like recipe : {recipe.id} : success')
                new_like.save()
                return Response(status=status.HTTP_201_CREATED)
            logger.debug(f'Exit like recipe : {recipe.id} {request.user} : failure')
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Error like recipe : {recipe.id} : {e}', exc_info=True)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            recipe = get_object_or_404(Recipe, id=self.kwargs['pk'])
            logger.debug(f'Enter dislike recipe : {request.user} {recipe.id}')
            like = RecipeLike.objects.filter(user=request.user, recipe=recipe)
            if like.exists():
                like.delete()
                logger.debug(f'Exit dislike recipe : {recipe.id} : success')
                return Response(status=status.HTTP_200_OK)
            logger.debug(f'Exit dislike recipe : {recipe.id} {request.user} : failure')
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Error dislike recipe : {recipe.id} : {e}', exc_info=True)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
