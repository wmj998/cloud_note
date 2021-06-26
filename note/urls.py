from django.urls import path, include

from note import views

urlpatterns = [
    path('add/', views.add),
    path('update/', views.update),
    path('delete/', views.delete),
    path('search/', views.search),
    path('result/', views.result),

]
