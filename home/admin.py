
from django.contrib import admin
from . models import *
# from . models import Contact, Product, Team, Profile
# Register your models here.

class ContactAdmin(admin.ModelAdmin):
    list_display = ['id','full_name', 'email', 'message','admin_note', 'status','message_data','admin_update']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','name','img', 'price', 'max_quantity', 'min_quantity', 'display','latest', 'trending', 'created', 'updated']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'first_name', 'last_name', 'email', 'phone', 'address', 'state','pix']

class ShopcartAdmin(admin.ModelAdmin):
    list_display = ('user','product', 'quantity','price','amount','order_no','paid','created_at')

class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'personnel','post']

admin.site.register(Contact, ContactAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Shopcart, ShopcartAdmin)
admin.site.register(Team, TeamAdmin)



