__author__ = 'indrajit'

from django.contrib import admin
from .models import *


class GroupMemberInline(admin.StackedInline):
    model = GroupMember


class GroupAdmin(admin.ModelAdmin):
    model = Group
    inlines = [GroupMemberInline, ]


class GroupMemberAdmin(admin.ModelAdmin):
    model = GroupMember


class FriendAdmin(admin.ModelAdmin):
    model = Friend


class CartItemInline(admin.StackedInline):
    model = CartItem


class CartAdmin(admin.ModelAdmin):
    model = Cart
    inlines = [CartItemInline, ]


class ShopperAdmin(admin.ModelAdmin):
    model = Shopper


admin.site.register(Cart, CartAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Friend, FriendAdmin)
admin.site.register(Shopper, ShopperAdmin)
