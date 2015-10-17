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
        fields = ('pk', 'user', 'name', 'get_members',)
        read_only_fields = ('get_members',)


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
        fields = ('cart', 'product', 'quantity', 'added_by',)


class CartItemListSerializer(serializers.ListSerializer):
    child = CartItemSerializer()

    def update(self, instance, validated_data):
        CartItem.objects.update_or_create(
            cart=instance.cart, product=instance.product,
            defaults={"cart": instance.cart, "product": instance.product, "quantity": instance.quantity}
        )
