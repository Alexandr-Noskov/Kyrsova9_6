from django.urls import path
from django.views.decorators.cache import never_cache

from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegisterView, UserUpdateView, generate_new_password

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', never_cache(RegisterView.as_view()), name='register'),
    path('profile/', never_cache(UserUpdateView.as_view()), name='profile'),
    path('profile/genpassword/', never_cache(generate_new_password), name='generate_new_password'),
]
