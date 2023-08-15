from django.urls import path, include
from . import views

 
urlpatterns = [
    path('', views.homePageView, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register', views.register, name='register'),
    path('facilities/', views.facilities, name='facilities'),
    path('activities/', views.activities, name='activities'),
    path('update_list/', views.update_list, name='update_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/get_pgl', views.api_get_pgl, name='api_get_pgl')
]

