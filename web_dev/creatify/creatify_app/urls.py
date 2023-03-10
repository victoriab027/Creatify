from django.urls import path
from . import views

app_name = 'creatify_app'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('base/', views.baserender, name='base'),
    path('results/', views.result_view, name='result_view'),
    path('authorize/', views.auth_view, name='auth'),
    # path('victoria/', views.vic_view, name='vic_view'),
]