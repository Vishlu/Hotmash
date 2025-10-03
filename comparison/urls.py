from django.contrib import admin
from django.urls import path
from comparison import views

urlpatterns = [
    path('', views.index, name='index'),
    path('vote/<int:image1_id>/<int:image2_id>/<int:winner_id>/', views.vote, name='vote'),
    path('recent-winner/', views.winner, name='recent_winner'),
]
