from django.contrib import admin
from. models import Products, Users, Admin, Category, Cart, Address
from django.contrib.admin import AdminSite

admin.site.register(Products)
admin.site.register(Users)
admin.site.register(Admin)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Address)

