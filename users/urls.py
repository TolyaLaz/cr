from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, email_verification, toggle_activity, UserDetailView, UserListView

app_name = UsersConfig.name

urlpatterns = [  # логин
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # регистрация
    path('register/', RegisterView.as_view(), name='register'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
    # пользователи
    path('profile/', ProfileView.as_view(), name='profile'),
    path('detail/<int:pk>/', UserDetailView.as_view(), name='view_user'),
    path('users_list/', UserListView.as_view(), name='view_all_users'),
    # бан
    path('toggle_activity/<int:pk>/', toggle_activity, name='toggle_activity'),
]