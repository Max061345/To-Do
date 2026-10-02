from rest_framework import serializers
from .models import Todo


class ToDoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'title', 'description', 'is_completed', 'created_at', 'user']
        read_only_fields = ['id', 'created_at', 'user']