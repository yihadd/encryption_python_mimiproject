from django.urls import path
from . import views

urlpatterns = [
    path('', views.encrypt_text, name='encrypt_text'),
    path('decrypt/', views.decrypt_text, name='decrypt_text'),
    path('download/', views.download_text, name='download_text'),
]
