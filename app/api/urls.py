from django.urls import path
from . import views

urlpatterns = [
    path('getdata/', views.getdata),
    path('adddata/', views.adddata),
    path('connectapi/', views.connectapi),
]