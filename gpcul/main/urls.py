from django.urls import path
from django.contrib.auth import views as auth_views
from .import views


urlpatterns = [
    path('',views.home, name = 'home'),
    path('login/',views.login_page, name = 'login'),
    path('register',views.register, name = 'register'),
    path('std_register/',views.std_register, name = 'std_register'),
    path('forget',views.forget, name = 'forget'),
    path('std_dash/', views.std_dash, name = "std_dash"),
    path('logout/', views.user_logout, name='logout'),
    
    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/forget.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/forget.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
