from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'cart'

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('login/', views.login_view, name='login'),  # Updated to use the custom login view
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='cart:login'), name='logout'),  # Redirects to login after logout
    path('products/', views.product_list, name="product_list"),
    path('add_products_to_cart/<int:product_id>/', views.add_products_to_cart, name="add_products_to_cart"),
    path('view_cart/', views.view_cart, name="view_cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('Order_successfull/<int:order_id>/', views.order_successfull, name="order_successfull"),
]
