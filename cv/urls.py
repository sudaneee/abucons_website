from django.urls import path
from . import views

urlpatterns = [
    path('', views.email_verification, name='email_verification'),
    path('verify-code/', views.verify_code, name='verify_code'),
    path('cv_submission/', views.cv_submission, name='cv_submission'),
    path('success/', views.success, name='success'),
]