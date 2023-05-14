from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('api-token-auth/', obtain_auth_token),
    path('manager/', views.managers),
    path('category/', views.CategoriesView.as_view()),
    path('menu-items/', views.MenuItemViews.as_view()),
]