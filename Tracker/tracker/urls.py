from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_expense, name='add_expense'),
    path('delete/<int:id>/', views.delete_expense, name='delete_expense'),
    path('register/', views.register, name='register'),
]