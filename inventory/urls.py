from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from inventory_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventory_app.urls')),  # This maps the root URL to app URLs
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]