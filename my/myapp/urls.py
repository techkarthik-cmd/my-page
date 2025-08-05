from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.projects_list, name='projects_list'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    
    path('mind/', views.mind, name='mind'),
    path('contact/', views.contact, name='contact'),

    # Profile (auth gate)
    path('profile/', views.profile_view, name='profile'),

    # Auth
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    
    path('auth/signup/', views.signup_view, name='signup'),
    path('auth/otp/', views.otp_request_view, name='otp_request'),
    path('auth/otp/verify/', views.otp_verify_view, name='otp_verify'),

    # Reset
    path('auth/reset/', views.ResetRequestView.as_view(), name='password_reset'),
    path('auth/reset/done/', views.ResetDoneView.as_view(), name='password_reset_done'),
    path('auth/reset/<uidb64>/<token>/', views.ResetConfirmView.as_view(), name='password_reset_confirm'),
    path('auth/reset/complete/', views.ResetCompleteView.as_view(), name='password_reset_complete'),
]

