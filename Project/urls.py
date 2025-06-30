from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),path('browse/', views.browse_cars, name='browse_cars'), path('login/', views.login_view, name='login') ,
    path('register/', views.register_view, name='register'), path('logout/', views.logout_view, name='logout'), path('list_your_car/', views.list_car_view, name='list_your_car'), path('order/<int:car_id>/', views.place_order, name='place_order'), path('place-order/', views.place_order, name='place_order'), path('place-order/<int:car_id>/', views.place_order, name='place_order_for_car')]


    
