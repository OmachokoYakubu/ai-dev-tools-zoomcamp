from django.urls import path
from . import views

urlpatterns = [
    path('', views.chore_list, name='chore_list'),
    path('chores/add/', views.add_chore, name='add_chore'),
    path('chores/<int:chore_id>/toggle/', views.toggle_chore_status, name='toggle_chore_status'),
    path('housemates/add/', views.add_housemate, name='add_housemate'),
]
