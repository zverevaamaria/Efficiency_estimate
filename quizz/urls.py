from django.urls import path
from . import views

urlpatterns = [
path('', views.index, name='index'),
path('calculation/', views.to_calculate, name='to_calculate'),
path('calculation/results/', views.to_result, name='to_result')
]
