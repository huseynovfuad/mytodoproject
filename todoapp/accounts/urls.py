from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/',views.login_view,name='login'),
    path('signup/',views.signup_view,name='signup'),
    path('logout/',views.logout_view,name='logout'),
    path('password-change/',views.password_change,name='password_change'),
]
