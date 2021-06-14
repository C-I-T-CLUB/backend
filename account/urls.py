from django.urls import path
from account import views

urlpatterns = [
    path('',views.index_page),
    path('signin',views.user_login),
    path('signup',views.user_registration),
    path('profile',views.user_profile),
    path('password_change',views.password_change),
    path('forgoten_password_change',views.forgoten_password_change),
    path('password_reset_code',views.password_reset_code),

]