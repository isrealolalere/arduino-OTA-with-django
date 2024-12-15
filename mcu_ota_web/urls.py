from mcu_ota_web import views
from django.urls import path

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login_url'),
    path('logout/', views.logout_view, name='logout'),

    path('upload_firmware/', views.upload_firmware, name='upload_firmware'),
    path('profile/', views.profile, name='profile'),

    path('mcu_api/get_firmware/', views.get_firmware, name='get_firmware'),
    path('mcu_api/ota_update/', views.ota_update, name='ota_update'),
    
]
