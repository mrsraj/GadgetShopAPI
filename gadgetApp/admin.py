from django.contrib import admin

# Register your models here.
from .models import ProductImage,Product,ProductSpecification,ProductPolicy

admin.site.register(ProductImage)
admin.site.register(Product)
admin.site.register(ProductSpecification)
admin.site.register(ProductPolicy)
