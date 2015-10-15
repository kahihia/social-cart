__author__ = 'indrajit'

from rest_framework import serializers

from .models import Shopper, Friend, Group, GroupMember

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

class GroupListSerializer(serializers.ModelSerializer, serializers.ListSerializer):
    class Meta:
        model = Group
        fields = ('pk', 'name', 'get_members',)

class GroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMember