from django.contrib import admin
from product.models import Product, Category, MiniCategory
# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(MiniCategory)
