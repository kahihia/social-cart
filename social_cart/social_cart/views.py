__author__ = 'indrajit'

import logging

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http.response import JsonResponse
from django.shortcuts import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.decorators import detail_route

from .serializers import ShopperSerializer, FriendSerializer, GroupListSerializer, GroupMemberSerializer, GroupSerializer
from .models import Shopper, Cart, CartItem, Friend, Group, GroupMember

logger = logging.getLogger(__name__)


def login(request):
    if request.method == 'GET':
        raise Http404

    try:
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        status = 'SUCCESS'
        if user is None:
            if User.objects.filter(Q(username=username) | Q(email=email)).count():
                status = 'FAIL'
                response = 'Username or email already exists. Please try again!'
            else:
                user = User.objects.create_user(username, email, password)
                response = 'Successfully signed up with Social Cart!'
        else:
            response = 'Successfully logged in to Social Cart!'

        return JsonResponse({'status': status, 'detail': response})

    except KeyError:
        raise Http404


class BaseApiView(APIView):
    permission_classes = (IsAuthenticated, )


class UserSearchView(BaseApiView):
    def get(self, request, format=None):
        try:
            param = self.request.GET['q']
        except KeyError as e:
            raise Http404
        shoppers = Shopper.objects.filter(Q(user__first_name__icontains=param) |
                                                Q(user__last_name__icontains=param) |
                                                Q(user__email__icontains=param) |
                                                Q(user__username__icontains=param))
        serializer = ShopperSerializer(shoppers, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class FriendsView(BaseApiView):
    def get_object(self, user):
        try:
            return Shopper.objects.get(user=user)
        except Shopper.DoesNotExist as e:
            logger.exception('User Not Found')
            raise Http404

    def get(self, request, format=None):
        user = self.get_object(request.user)
        friends = user.get_friends()
        serializer = ShopperSerializer(friends, many=True)
        return Response(serializer.data, HTTP_200_OK)

    def put(self, request, shopper_id, format=None):
        user = self.get_object(request.user)
        friend = self.get_object(shopper_id)
        friendship = user.add_friend(friend)
        serializer = FriendSerializer(friendship)
        return Response(serializer.data, status=HTTP_201_CREATED)

    def delete(self, request, shopper_id, format=None):
        user = self.get_object(shopper_id)
        friend = self.get_object(shopper_id)
        user.remove_friends(friend)
        return Response({'status': 'SUCCESS', 'detail': 'Removed friend'}, status=HTTP_204_NO_CONTENT)


class GroupViewSet(BaseApiView, ModelViewSet):
    def get_shopper(self, shopper_id):
        try:
            return Shopper.objects.get(user=shopper_id)
        except Shopper.DoesNotExist as e:
            logger.exception('User Not Found')
            raise Http404

    def get_object(self, user, group_id):
        try:
            return Group.objects.get(user=user, pk=group_id)
        except Shopper.DoesNotExist as e:
            logger.exception('Group Not Found')
            raise Http404

    def retrieve(self, request, format=None):
        user = self.get_shopper(request.user)
        groups = Group.objects.filter(user=user)
        serializer = GroupListSerializer(groups)
        return Response(serializer.data, status=HTTP_200_OK)

    def create(self, request, format=None):
        group_name = self.request.POST['group_name']
        user = self.get_shopper(request.user)
        group = Group.objects.create(name=group_name, user=user)
        serializer = GroupSerializer(group)
        return Response(serializer.data, HTTP_201_CREATED)

    @detail_route(methods=['put'])
    def add_list_friend(self, request, group_id, format=None):
        user = self.get_shopper(request.user)
        group = self.get_object(user, group_id)
        try:
            friend = self.get_shopper(self.request.GET['friend'])
            if not user.is_friend(friend):
                raise ValueError
            member = GroupMember.objects.create(group, friend)
            serializer = GroupMemberSerializer(member)
            return Response(serializer.data, HTTP_201_CREATED)
        except KeyError as e:
            logger.info('Friend parameter missing')
            raise Http404
        except ValueError as e:
            logger.exception('User is not in friends list')
            raise Http404

    @detail_route(methods=['delete'])
    def delete_list_friend(self, request, group_id, format=None):
        user = self.get_shopper(request.user)
        group = self.get_object(user, group_id)
        try:
            friend = self.get_shopper(self.request.GET['friend'])
            if not user.is_friend(friend):
                raise ValueError
            GroupMember.objects.filter(group, friend).delete()
            return Response({'status': 'SUCCESS', 'detail': 'Successfully removed from List'}, HTTP_204_NO_CONTENT)
        except KeyError as e:
            logger.info('Friend parameter missing')
            raise Http404
        except ValueError as e:
            logger.exception('User is not in friends list')
            raise Http404
