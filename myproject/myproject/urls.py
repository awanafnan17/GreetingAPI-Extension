# myproject/urls.py
from django.contrib import admin
from django.urls import path, include
from myproject.views import my_view, your_secured_endpoint
from myapp import views


urlpatterns = [
    path('', my_view, name='my-view'),  # Define the root URL pattern
    path('admin/', admin.site.urls),
    path('myapp/', include('myapp.urls')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('api/your-secured-endpoint/', your_secured_endpoint, name='your-secured-endpoint'),
    path('test-submit-greeting/', views.test_submit_greeting, name='test-submit-greeting'),
]