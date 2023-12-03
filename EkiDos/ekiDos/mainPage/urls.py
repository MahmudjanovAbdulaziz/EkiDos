from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *

app_name = 'mainPage'


urlpatterns = [
    path('', index, name='index'),
    path('search/', search_view, name='search'),
    path('logout/', logout_view, name='logout'),
    path('chat/', chatView, name='chat'),
    path('like_comment/<int:comment_id>/', like_comment, name='like_comment'),
    path('cart/view/', view_cart, name='view_cart'),
    path('cart/add/', add_to_cart, name='add_to_cart'),
    path('delete_product/<int:product_id>/', delete_product_in_cart, name='delete_product_in_cart'),
    path('profile/', profile, name='profile'),
    path('profile/add/', add_profile, name='add_profile'),

]
