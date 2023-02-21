from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('base/', views.baserender, name='base'),
    path('result/', views.result_view, name='result_view'),
]