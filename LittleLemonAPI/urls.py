from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('api-token-auth/', obtain_auth_token),
    path('manager/', views.managers),
    path('category/', views.CategoriesView.as_view()),
    path('menu-items/', views.MenuItemViews.as_view()),
    path('cart/menu-items/', views.CartView.as_view()),
    path('orders/menu-items/', views.OrderView.as_view()),
    # path('orders/', views.OrdersView.as_view()),
    # path('orders/<int:pk>/', views.SingleOrderVIew.as_view(), name="order_item")
]