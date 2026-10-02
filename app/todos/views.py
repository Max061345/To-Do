from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Todo
from .serializers import ToDoSerializer
import logging
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView


logger = logging.getLogger('todos')


class ToDoViewSet(viewsets.ModelViewSet):
    serializer_class = ToDoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        try:
            instance = serializer.save(user=self.request.user)
            logger.info(f"User {self.request.user.username} created case succesfully ID {instance.id}")
        except Exception as e:
            logger.error(f"Creation error by user {self.request.user.username}: {str(e)}")
            raise

    def perform_destroy(self, instance):
        task_id = instance.id
        try:
            super().perform_destroy(instance)

            logger.info(f"User {self.request.user.username} deleted case ID {task_id}")
        except Exception as e:
            logger.error(f"Case deleting error {task_id}: {str(e)}")
            raise


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            logger.info(f"User {user.username} entered into the system succesfully")

            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            })

        except Exception as e:
            logger.error(f"Error while entering system (maybe incorrect data). Details: {str(e)}")
            raise
