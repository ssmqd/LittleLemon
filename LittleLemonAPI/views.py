from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, generics
from .models import MenuItem, Category, Cart, Order
from .serializers import MenuItemSerializer, CategorySerializer, CartSerializer, OrderSerializer
from django.shortcuts import render

@api_view(['POST'])
@permission_classes([IsAdminUser])
def managers(request):
	username = request.data['username']
	if username:
		user = get_object_or_404(User, username=username)
		managers = Group.objects.get(name="Manager")
		if request.method == 'POST':
			managers.user_set.add(user)
		if request.method == 'DELETE':
			managers.user_set.remove(user)
		return Response({'message':f'user {username} successfully added'})
	
	return Response({"message": "error"}, status.HTTP_400_BAD_REQUEST)


class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]


class MenuItemViews(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer	
    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]
    ordering_fields = ['price']
    filtering_fields = ['category']
    search_fields = ['title']
    
    def get(self, request):
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('price')
        search = request.query_params.get('search')
        
        if category_name:
            self.queryset = self.queryset.filter(category__slug = category_name)
        if to_price:
            self.queryset = self.queryset.filter(price = to_price)
        if search:
            self.queryset = self.queryset.filter(category__slug__startswith = search)
        return super().get(request)

class CartView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer	
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# class OrdersView(generics.ListCreateAPIView):
#     queryset = Orders.objects.all()
#     serializer_class = OrderSerializer

#     # def retrieve(self, request, *args, **kwargs):
#     #     instance = self.get_object()
#     #     serializer = self.get_serializer(instance)

#     #     menu_items = serializer.data['menu_items']
#     #     total_price = sum(item['price'] for item in menu_items)

#     #     serializer.data['total_price'] = total_price
#     #     return Response(serializer.data)

#     def post(self, request):
#         user = request.user
#         cart = Cart.objects.filter(user=user)
#         if cart.exists():
#             cart_data = []
#             for carts in cart:
#                 order = Orders()
#                 order.order = user
#                 order.menuitem = carts.menuitem
#                 order.quantity = carts.quantity
#                 order.unit_price = carts.unit_price
#                 order.price = carts.price
#                 order.save()
#                 serializer = OrderSerializer(order)
#                 cart_data.append(CartSerializer.data)
#             return Response(serializer.data)
#         else:
#             return Response({"error": "Cart does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
# class SingleOrderVIew(generics.ListCreateAPIView):
#     queryset = Orders.objects.all()
#     serializer_class = OrderSerializer
#     def get(self, request, pk):
#         order = Orders.objects.get(order=pk)
#         if order.exists():
#             serializer = OrderSerializer(order, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "Order does not exist"}, status=status.HTTP_404_NOT_FOUND)