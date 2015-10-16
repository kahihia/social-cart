__author__ = 'indrajit'

from rest_framework import serializers

from .models import Shopper, Friend, Group, GroupMember, Product, CartInvite, Cart, CartItem


class ShopperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shopper
        fields = (
            'pk',
            'user',
            'username',
            'email',
        )


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('pk', 'name', 'get_members',)
        read_only_fields = ('name', 'get_members',)


class GroupListSerializer(serializers.ModelSerializer, serializers.ListSerializer):
    class Meta:
        model = Group
        fields = ('pk', 'name', 'get_members',)
        read_only_fields = ('name', 'get_members',)


class GroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMember


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product


class CartInviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartInvite
        fields = ('get_owner_name', 'get_cart_id', )

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('cart', 'product', 'item_id', 'quantity',)
        read_only_fields = ('item_id', 'quantity',)