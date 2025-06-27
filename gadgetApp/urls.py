from django.urls import path
from .views import RegisterView,LoginView,ProtectedView,AdminOnlyView,TeacherOnlyView,StudentOnlyView
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView

from .views import(product_list, product_detail,cart_list,
                   cart_detail,address_list, 
                   address_detail,order_list, order_detail,
                   orderitem_list, orderitem_detail,
                   payment_list, payment_detail,
                   category_list,category_detail,
                   brand_list,brand_detail,
                   cartitem_list,cartitem_detail,
                   product_image_list, product_image_detail
                )


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
    path('categories/', category_list, name='category-list'),
    path('categories/<int:pk>/', category_detail, name='category-detail'),
    
    path('brands/', brand_list, name='brand-list'),
    path('brands/<int:pk>/', brand_detail, name='brand-detail'),
    
    path('products/', product_list, name='brand-list'),
    path('products/<int:pk>/', product_detail, name='brand-detail'),
    
    path('carts/', cart_list, name='cart-list'),
    path('carts/<int:pk>/', cart_detail, name='cart-detail'),
    
    path('addresses/', address_list, name='address-list'),
    path('addresses/<int:pk>/', address_detail, name='address-detail'),
    
    path('orders/', order_list, name='order-list'),
    path('orders/<int:pk>/', order_detail, name='order-detail'),
    
    path('order-items/', orderitem_list, name='orderitem-list'),
    path('order-items/<int:pk>/', orderitem_detail, name='orderitem-detail'),
    
    path('payments/', payment_list, name='payment-list'),
    path('payments/<int:pk>/', payment_detail, name='payment-detail'),
    
    path('cart-items/', cartitem_list, name='cartitem-list'),
    path('cart-items/<int:pk>/', cartitem_detail, name='cartitem-detail'),
    
    path('product-images/', product_image_list, name='productimage-list'),
    path('product-images/<int:pk>/', product_image_detail, name='productimage-detail'),
]


## """Create items in order: Category → 
# Brand → Product → Cart → CartItem → Address → Order → OrderItem → Payment."""