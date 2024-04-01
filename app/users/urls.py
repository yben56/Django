from django.urls import path
from . import views
from .middleware import AuthenticationMiddleware

urlpatterns = [
    path('signup/', views.signup),
    path('email_confirmation/', views.email_confirmation),
    path('login/', views.login),
    path('logout/', views.logout),
    path('reset_password/', views.reset_password),

    path('user/', AuthenticationMiddleware(views.user)),
]