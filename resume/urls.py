from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProfileView.as_view(), name="home"),
    path('create', views.create_profile, name="create_profile"),
]
