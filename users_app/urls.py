from django.urls import path, include
from users_app import views

app_name='users_app'
urlpatterns = [
    path('logout/',views.user_logout,name='logout'),
    path('special/',views.special,name='special'),
    #path('register/',views.register,name='register'),
    path('login/',views.user_login,name='user_login'),
    path('generate_account/',views.generate_account,name='generate_account'),
]
