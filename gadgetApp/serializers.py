from rest_framework import serializers
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from .models import *

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        role_name = validated_data.pop('role', None)
        user = User.objects.create_user(**validated_data)

        if role_name:
            group, _ = Group.objects.get_or_create(name=role_name)
            user.role = group
            user.groups.add(group)  # Assign role to user
            user.save()

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    
## New Code 

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source='cartitem_set', many=True, read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_amount', 'status', 'created_at', 'updated_at', 'shipping_address', 'items']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        


###New Special code for product:

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image_file', 'image_url']

class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = ['id', 'key', 'value']

class ProductPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPolicy
        fields = ['id', 'delivery_note', 'delivery_charge']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    specs = ProductSpecificationSerializer(many=True, read_only=True)
    policies = ProductPolicySerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'brand', 'name', 'description',
            'stock_quantity', 'ram', 'processor', 'storage',
            'actual_price', 'offer_price', 'discount_percent',
            'created_at', 'updated_at',
            'images', 'specs', 'policies'
        ]
        
class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields = ['category', 'brand', 'name', 'description',
            'stock_quantity', 'ram', 'processor', 'storage',
            'actual_price', 'offer_price', 'discount_percent'
        ]


## Set Image 
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'image_file', 'image_url']