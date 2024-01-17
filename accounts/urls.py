from django.urls import path,include
from . import views

app_name='accounts'

urlpatterns=[
    path('',views.LoginUser.as_view(),name='login'),
    path('logout/',views.logout,name='logout'),
    path('Register/',views.RegisterUser.as_view(),name='Register'),
    path('api/v1/',include('accounts.api.v1.urls'))
]