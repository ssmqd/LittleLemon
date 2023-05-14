from rest_framework import serializers
from .models import MenuItem, Category, Cart, Order, UserGroup
from rest_framework.fields import CurrentUserDefault
from django.contrib.auth.models import User, AnonymousUser

class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title']

class MenuItemSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)
    class Meta:
        model = MenuItem
        fields = ['title', 'price', 'featured', 'category', 'category_id']
        extra_kwargs = {
            'price': {'min_value': 2},
            'inventory':{'min_value':0}
        }

class CartSerializer(serializers.ModelSerializer):
    unit_price = serializers.DecimalField(source='menuitem.price', max_digits=6, decimal_places=2, read_only=True)
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

    

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order', 'menuitem', 'quantity', 'unit_price', 'price']
        