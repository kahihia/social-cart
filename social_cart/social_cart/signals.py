__author__ = 'indrajit'

import logging
import settings

from allauth.socialaccount.signals import social_account_added
from allauth.socialaccount.models import SocialLogin, SocialAccount, SocialToken
from facepy import GraphAPI
from googleapiclient.discovery import build

from django.db.models.signals import post_save

from .models import Shopper

logger = logging.getLogger(__name__)

google_plus_service = build(serviceName='plus', version='v1', developerKey=settings.GOOGLE_PLUS_API_KEY)
people = google_plus_service.people()


def build_facebook_friendship(token):
    try:
        shopper_a = Shopper.objects.get_or_create(user=token.user)

        graph = GraphAPI(oauth_token=token.token)
        friends = graph.get('me/friends/')

        logger.info(friends)

        for friend in friends['data']:
            try:
                friend_user = SocialAccount.objects.get(uid=friend['id'])
            except SocialAccount.DoesNotExist as e:
                logger.exception('User should exist but does not. Weird')
                continue
            shopper_b = Shopper.objects.get_or_create(friend_user.user)
            shopper_a.add_friend(shopper_b)
    except Exception as e:
        logger.exception(e)


def build_google_friendship(token):
    try:
        shopper_a = Shopper.objects.get_or_create(user=token.user)

        friends = people.list(userId=token.token, collections='visible')

        for friend in friends['items']:
            try:
                friend_user = SocialAccount.objects.get(uid=friend['id'])
            except SocialAccount.DoesNotExist as e:
                logger.exception('User should exist but does not. Weird')
                continue
            shopper_b = Shopper.objects.get_or_create(friend_user.user)
            shopper_a.add_friend(shopper_b)
    except Exception as e:
        logger.exception(e)


def friendify(sender, instance, **kwargs):
    """
    Find existing social friends in App and build the relation
    """
    account = instance.account
    token = instance.token
    provider = account.provider
    if provider == 'facebook':
        build_facebook_friendship(token=token)
    elif provider == 'google':
        build_google_friendship(token=token)
    else:
        logging.exception('Unknown Provider')

social_account_added.connect(friendify, sender=SocialLogin)
