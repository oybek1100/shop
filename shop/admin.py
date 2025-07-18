from django.contrib import admin
from .models import Product , Category , OrderDetail  , Comment
from django.contrib.auth.models import User, Group 


admin.site.register(Category)
admin.site.register(OrderDetail)
admin.site.register(Comment)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'discount' ,'category' , 'created_at' , 'quantity']
    list_filter = ['price' , 'category' , 'created_at']

admin.site.site_header = "My Shop Admin"
# admin.site.site_title = "My Shop Admin Portal"
admin.site.index_title = "Welcome to My Shop Admin Portal"
 


