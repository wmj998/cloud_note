from django.urls import path, include

from user import views

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login_user),
    path('index/', views.index),
    path('logout/', views.logout_user),
    path('delete/', views.delete),
]
