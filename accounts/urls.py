from django.urls import path
from . import views 

urlpatterns = [
    path('user-login/', views.UserLoginView, name='user_log'),
    path('user-logout/', views.logout_view, name='user_out'),
]