from django.urls import path,include
from .views import *
app_name="ajax"
urlpatterns = [
   path('login',login,name='login'),
   path('register',register,name='register'),
   path('update_user',update_user,name='update_user'),
   path('cep_update',cep_update,name='cep_update'),
   path('update_password',update_password,name='update_password'),
   path('update_avatar',update_avatar,name='update_avatar'),
   path('borsa',borsa_cek,name='borsa_cek'),
   path('machinebuy',MachineBuy,name='machinebuy'),
   path('payment',payment,name='payment'),
   path('request_payment',request_payment,name='request_payment'),
   path('request_code',request_code,name='request_code')
]