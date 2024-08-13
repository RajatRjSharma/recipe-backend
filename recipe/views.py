from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from .models import Recipe, RecipeLike
from .serializers import RecipeLikeSerializer, RecipeSerializer
from .permissions import IsAuthorOrReadOnly
from .filter import *

import logging

logger = logging.getLogger(__name__)


class RecipeViewSet(viewsets.ModelViewSet):
    """
    list: Get a collection of recipes
    create: Create a recipe
    retrieve: Get a single recipe
    update: Update a recipe
    destroy: Delete a recipe
    """

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        elif self.action == "create":
            return [IsAuthenticated()]
        else:
            return [IsAuthorOrReadOnly()]

    def list(self, request, *args, **kwargs):
        try:
            logger.debug("Enter get list of recipes")
            response = super().list(request, *args, **kwargs)
            logger.debug("Exit get list of recipes: success")
            return response
        except Exception as e:
            logger.error(f"Error get list of recipes: {e}", exc_info=True)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        try:
            logger.debug("Enter create recipe")
            response = super().create(request, *args, **kwargs)
            logger.debug("Exit create recipe: success")
            return response
        except Exception as e:
            logger.error(f"Error create recipe: {e}", exc_info=True)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        try:
            logger.debug(f'Enter get recipe detail: {self.kwargs["pk"]}')
            response = super().retrieve(request, *args, **kwargs)
            logger.debug(f'Exit get recipe detail: {self.kwargs["pk"]}: success')
            return response
        except Exception as e:
            logger.error(
                f'Error get recipe detail: {self.kwargs["pk"]}: {e}', exc_info=True
            )
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            logger.debug(f'Enter update recipe detail: {self.kwargs["pk"]}')
            response = super().update(request, *args, **kwargs)
            logger.debug(f'Exit update recipe detail: {self.kwargs["pk"]}: success')
            return response
        except Exception as e:
            logger.error(
                f'Error update recipe detail: {self.kwargs["pk"]}: {e}', exc_info=True
            )
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            logger.debug(f'Enter delete recipe: {self.kwargs["pk"]}')
            response = super().destroy(request, *args, **kwargs)
            logger.debug(f'Exit delete recipe: {self.kwargs["pk"]}: success')
            return response
        except Exception as e:
            logger.error(
                f'Error delete recipe: {self.kwargs["pk"]}: {e}', exc_info=True
            )
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RecipeLikeAPIView(generics.CreateAPIView):
    """
    Like, Dislike a recipe
    """

    serializer_class = RecipeLikeSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        try:
            recipe = get_object_or_404(Recipe, id=self.kwargs["pk"])
            logger.debug(f"Enter like recipe : {request.user} {recipe.id}")
            new_like, created = RecipeLike.objects.get_or_create(
                user=request.user, recipe=recipe
            )
            if created:
                logger.debug(f"Exit like recipe : {recipe.id} : success")
                new_like.save()
                return Response(status=status.HTTP_201_CREATED)
            logger.debug(f"Exit like recipe : {recipe.id} {request.user} : failure")
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error like recipe : {recipe.id} : {e}", exc_info=True)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            recipe = get_object_or_404(Recipe, id=self.kwargs["pk"])
            logger.debug(f"Enter dislike recipe : {request.user} {recipe.id}")
            like = RecipeLike.objects.filter(user=request.user, recipe=recipe)
            if like.exists():
                like.delete()
                logger.debug(f"Exit dislike recipe : {recipe.id} : success")
                return Response(status=status.HTTP_200_OK)
            logger.debug(f"Exit dislike recipe : {recipe.id} {request.user} : failure")
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error dislike recipe : {recipe.id} : {e}", exc_info=True)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
