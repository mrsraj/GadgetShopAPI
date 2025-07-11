from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import get_user_model

##New Code:---
from rest_framework.decorators import api_view,parser_classes,permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.parsers import MultiPartParser, FormParser

from .permissions import IsAdmin, IsTeacher, IsStudent

User = get_user_model()

# Register User API
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login API (JWT Token Generation)
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            user = authenticate(username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)

                # Get user's role (group name)
                groups = user.groups.all()
                print("Group = ",groups[0])
                role = groups[0].name if groups.exists() else "No Role"

                return Response({
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "role": role
                }, status=status.HTTP_200_OK)

            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Protected API for Testing
class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "This is a protected route", "user": request.user.username})



# Admin-Only View
class AdminOnlyView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        return Response({"message": "Welcome, Admin!"})

# Teacher-Only View
class TeacherOnlyView(APIView):
    permission_classes = [IsTeacher]

    def get(self, request):
        return Response({"message": "Welcome, Teacher!"})

# Student-Only View
class StudentOnlyView(APIView):
    permission_classes = [IsStudent]

    def get(self, request):
        return Response({"message": "Welcome, Student!"})
    
    
## new code

@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()

    # Filters from query params
    ram = request.GET.get('ram')
    storage = request.GET.get('storage')
    brand = request.GET.get('brand')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if ram:
        products = products.filter(ram__iexact=ram)

    if storage:
        products = products.filter(storage__iexact=storage)

    if brand:
        products = products.filter(brand__iexact=brand)

    if min_price and max_price:
        products = products.filter(offer_price__gte=min_price, offer_price__lte=max_price)
    elif min_price:
        products = products.filter(offer_price__gte=min_price)
    elif max_price:
        products = products.filter(offer_price__lte=max_price)

    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view(['POST'])
def product_create(request):
    serializer = ProductCreateSerializer(data=request.data)
    if serializer.is_valid():
        product = serializer.save()
        return Response(ProductCreateSerializer(product).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def create_product_image(request):
    serializer = ProductImageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



## Cart Function

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def cart_list_create(request):
    if request.method == 'GET':
        items = CartItem.objects.all()
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cart_delete(request, pk):
    try:
        item = CartItem.objects.get(pk=pk)
    except CartItem.DoesNotExist:
        return Response({'error': 'CartItem not found'}, status=status.HTTP_404_NOT_FOUND)

    item.delete()
    return Response({'message': 'CartItem deleted'}, status=status.HTTP_204_NO_CONTENT)


## WISH LIST VIEWS

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def wishlist_list_create(request):
    if request.method == 'GET':
        items = Wishlist.objects.all()
        serializer = WishlistSerializer(items, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("data=request.data = ", request.data)
        serializer = WishlistSerializer(data=request.data)

        user = request.data.get('user')
        product = request.data.get('product')

        if Wishlist.objects.filter(user=user, product=product).exists():
            return Response({"detail": "Product is already in the wishlist."}, status=status.HTTP_200_OK)

        if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated]) 
def wishlist_delete(request, pk):
    try:
        item = Wishlist.objects.get(pk=pk)
    except Wishlist.DoesNotExist:
        return Response({'error': 'Wishlist item not found'}, status=status.HTTP_404_NOT_FOUND)

    # Optional: Ensure user can only delete their own wishlist
    if item.user != request.user:
        return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

    item.delete()
    return Response({'message': 'Wishlist item deleted'}, status=status.HTTP_204_NO_CONTENT)