from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ToDoViewSet

router = DefaultRouter()
router.register(r'', ToDoViewSet, basename='todo')

urlpatterns =  [
    path('', include(router.urls)),    
]