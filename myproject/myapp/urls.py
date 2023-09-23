# myapp/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GreetingViewSet
from myapp import views


router = DefaultRouter()
router.register(r'greetings', GreetingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('my-template/', views.my_view, name='my-template'),
    path('test-submit-greeting/', views.test_submit_greeting, name='test-submit-greeting'),
]
