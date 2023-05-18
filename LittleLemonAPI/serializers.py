from rest_framework import serializers
from .models import MenuItem, Category, Cart, Order, OrderItem
from django.contrib.auth.models import AnonymousUser
from datetime import date

class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']
        extra_kwargs = {
            'price': {'min_value': 2},
            'inventory':{'min_value':0}
        }

class CartSerializer(serializers.ModelSerializer):
    # unit_price = serializers.PrimaryKeyRelatedField(MenuItem)
    price = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['user', 'menuitem', 'quantity', 'unit_price', 'price']
    
    def get_price(self, obj):
        return obj.unit_price * obj.quantity

    def get_user(self, obj):
        user = self.context['request'].user
        if isinstance(user, AnonymousUser):
            return None
        else:
            return user.id

    def create(self, data):
        menuitem = data['menuitem']
        unit_price = menuitem.price
        # user = self.context['request'].user
        # data['user'] = user
        data['unit_price'] = unit_price
        data['price'] = data['quantity'] * data['unit_price']
        return super().create(data)

    

# class OrderSerializer(serializers.ModelSerializer):

#     order = serializers.PrimaryKeyRelatedField(read_only=True)
#     menuitem = serializers.PrimaryKeyRelatedField(read_only=True)
#     quantity = serializers.IntegerField(read_only=True)
#     unit_price = serializers.DecimalField(read_only=True, max_digits=6, decimal_places=2)
#     price = serializers.DecimalField(read_only=True, max_digits=6, decimal_places=2)

#     class Meta:
#         model = Orders
#         fields = ['order', 'menuitem', 'quantity', 'unit_price', 'price']

    
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order', 'menuitem', 'quantity', 'unit_price', 'price']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(read_only = True, many = True)
    class Meta:
        model = Order
        fields = ('id', 'user', 'delivery_crew', 'status', 'order_items', 'total', 'date')

class OrderDetailSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(read_only = True, many = True)
    class Meta:
        model = Order
        fields = ('order_items')
