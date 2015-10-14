__author__ = 'indrajit'

from rest_framework import serializers

from .models import SocialShopper, SocialFriends, SocialGroup, SocialGroupMember

class SocialShopperSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialShopper


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialFriends

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialGroup
        fields = ('pk', 'name', 'get_members',)

class GroupListSerializer(serializers.ModelSerializer, serializers.ListSerializer):
    class Meta:
        model = SocialGroup
        fields = ('pk', 'name', 'get_members',)

class GroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialGroupMember