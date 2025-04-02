from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns=[
    path('',home,name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('online_food/',online_food,name='online_food'),
    path('food/<int:food_id>/', food_item_detail, name='food_detail'),
    path('restaurant/',restaurant,name='restaurant'),
    path('restaurant/<int:restaurant_id>/', restaurant_detail, name='restaurant_detail'),
    path('music/', music_events, name='music_events'),
    path('veg/',veg,name='veg'),
    path('non_veg/',non_veg,name='non_veg'),
    path('snacks/',snacks,name='snacks'),

    path('contact/', contact_view, name='contact'),
    path('contact/success/', contact_success_view, name='contact_success'),
   

    path('add-to-cart/<int:food_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart_view'),
    path('increase-cart-item/<int:cart_id>/', increase_cart_item, name='increase_cart_item'),
    path('decrease-cart-item/<int:cart_id>/', decrease_cart_item, name='decrease_cart_item'),
    path('remove-from-cart/<int:cart_id>/', remove_from_cart, name='remove_from_cart'),

    path('place-order/', place_order, name='place_order'),
    path('order-success/', order_success, name='order_success'),  

    path('book/<int:restaurant_id>/', book_restaurant, name='book_restaurant'),
    path('booking-success/<int:restaurant_id>/', booking_success, name='restaurant_success'),

   
    path('book/', book_show, name='book_show'),
    path('success/', booking_show_success, name='booking_show_success'),

    path('logout/', logout_view, name='logout'),
    
    path('cart-count/', cart_count_api, name='cart_count_api'),
    path('search/', search_view, name='search'),
    path('restaurants/',restaurant_view, name='restaurant_view'),
    path('food-search/', food_search_view, name='food_search_view'),
    path('music-search/',music_search_view, name='music_search_view'),
    path('veg-search/',veg_search_view, name='veg_search_view'),
    path('non-veg-search/', non_veg_search_view, name='non_veg_search_view'),
    path('snacks-drinks-search/', snacks_drinks_search_view, name='snacks_drinks_search_view'),

    path('edit-profile/', edit_profile_view, name='edit_profile_view'),


    
    
    path('password-reset/', forgot_password, name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', reset_password, name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),


    # path('order-summary/<int:order_id>/', order_summary, name='order_summary'),



    
]



