from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('dashboard/', views.dashboard),
    path('dashboard/add-game', views.add_game),
    path('game/<int:id>', views.game_details),
    path('dashboard/logout', views.logout),
    path('flush/', views.flush),
    path('edit/game/<int:id>/', views.edit_data),
    path('update', views.change_data),
    path('<int:id>/delete', views.delete)

]