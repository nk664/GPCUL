from django.urls import path
from .import views


urlpatterns = [
    path('',views.home, name = 'home'),
    path('login/',views.login, name = 'login'),
    path('register',views.register, name = 'register'),
    path('std_register/',views.std_register, name = 'std_register'),
    path('forget',views.forget, name = 'forget'),
    

    ]