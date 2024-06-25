from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Customer, Product, Cart, OrderPlaced

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality', 'city', 'zipcode', 'state']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discounted_price', 'description', 'brand', 'category', 'product_image']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']


@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'customer_link', 'product_info', 'product', 'quantity', 'order_date', 'status']
    
    def customer_link(self, obj):
        if obj.customer:
            link = reverse("admin:app_customer_change", args=[obj.customer.pk])
            return format_html('<a href="{}">{}</a>', link, obj.customer.name)
        return "-"
    
    customer_link.short_description = 'Customer Info'
    
    def product_info(self, obj):
        if obj.product:
            link = reverse("admin:app_product_change", args=[obj.product.pk])
            # Debugging line to print all attributes of the product
            print(vars(obj.product))
            return format_html('<a href="{}">{}</a>', link, obj.product.title)  # Replace 'title' with correct field name
        return "-"
    
    product_info.short_description = 'Product Info'