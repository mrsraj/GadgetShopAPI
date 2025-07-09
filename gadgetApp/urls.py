from django.urls import path
from .views import RegisterView,LoginView,ProtectedView,AdminOnlyView,TeacherOnlyView,StudentOnlyView
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView

from . import views

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('admin-only/', AdminOnlyView.as_view(), name='admin_only'),
    path('teacher-only/', TeacherOnlyView.as_view(), name='teacher_only'),
    path('student-only/', StudentOnlyView.as_view(), name='student_only'),
    
    ## New Code
    
    path('products/', views.product_list, name='product-list'),
    path('products/<int:pk>/', views.product_detail, name='product-detail'),
    path('product-images/create/', views.create_product_image, name='product-image-create'),
    path('products/create/', views.product_create, name='product-create'),
    
    ## Wish list and add to cart
    path('cart/', views.cart_list_create, name='cart-list-create'),
    path('cart/<int:pk>/del', views.cart_delete, name='cart-delete'),

    # Wishlist URLS
    path('wishlist/', views.wishlist_list_create, name='wishlist-list-create'),
    path('wishlist/<int:pk>/del', views.wishlist_delete, name='wishlist-delete'),
]


## """Create items in order: Category → 
# Brand → Product → Cart → CartItem → Address → Order → OrderItem → Payment."""

# /products/?ram=8GB

# /products/?storage=512GB

# /products/?brand=HP

# /products/?min_price=30000&max_price=60000

# /products/?ram=16GB&brand=Lenovo&min_price=40000