__author__ = 'indrajit'

import logging

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

logger = logging.getLogger(__name__)

CART_TYPES = (
    ('P', 'Personal'),
    ('S', 'Social'),
)


class Shopper(models.Model):
    user = models.ForeignKey(User)
    gcm_key = models.CharField(max_length=400, null=True, blank=True)

    def __unicode__(self):
        return self.user.username

    @property
    def username(self):
        return self.user.username

    @property
    def email(self):
        return self.user.email

    def is_friends(self, friend):
        return Friend.is_friend(self, friend)

    def add_friend(self, friend):
        return Friend.add_friends(self, friend)

    def remove_friend(self, fried):
        return Friend.remove_friends(self, fried)

    def get_friends(self):
        return Friend.get_friends(self)

    def notify_cart_created(self, cart):
        from .gcm import send_gcm_notification
        inviter = cart.user.user.username.title()
        data = {
            'notification': {
                'title': '{} created a Social Cart!'.format(inviter),
                'message': 'Start adding stuff to it!'.format(inviter)
            },
            'to': self.gcm_key
        }
        send_gcm_notification(data)

    def notify_cart_finalized(self, cart):
        from .gcm import send_gcm_notification
        inviter = cart.user.user.username.title()
        data = {
            'notification': {
                'title': '{} is done Shopping!'.format(inviter),
                'message': '{} has picked up your stuff! Cheers!'.format(inviter)
            },
            'to': self.gcm_key
        }
        send_gcm_notification(data)


class Product(models.Model):
    name = models.CharField(max_length=300)
    item_id = models.BigIntegerField(unique=True)
    msrp = models.FloatField()
    sale_price = models.FloatField()
    upc = models.BigIntegerField()
    shortDescription = models.CharField(max_length=500)
    url = models.URLField(max_length=300)
    image_url = models.URLField(max_length=300)
    brand_name = models.CharField(max_length=100)
    rating = models.FloatField()
    rating_url = models.URLField(max_length=300)
    stock = models.CharField(max_length=20)
    reviews = models.IntegerField()

    def __unicode__(self):
        return '{}-{}-{}'.format(self.id, self.item_id, self.name[:15])


class Cart(models.Model):
    user = models.ForeignKey(Shopper, related_name='carts')
    type = models.CharField(choices=CART_TYPES, max_length=2)
    is_active = models.BooleanField(default=True)

    def finalize(self):
        self.is_active = False
        self.save()
        for invitee in self.cartinvitees.all():
            invitee.notify_cart_finalized(self)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cartitems')
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField('Added At', auto_now_add=True)
    updated_at = models.DateTimeField('Updated At', auto_now_add=True)
    added_by = models.ForeignKey(Shopper)


class CartInvite(models.Model):
    owner = models.ForeignKey(Shopper, related_name='owner')
    cart = models.ForeignKey(Cart, related_name='cartinvitees')
    invitee = models.ForeignKey(Shopper, related_name='invitees')
    is_active = models.BooleanField()

    @property
    def get_cart_id(self):
        return self.cart.pk

    @property
    def get_owner_name(self):
        return self.owner.user.username


class Friend(models.Model):
    friend_one = models.ForeignKey(Shopper, related_name='friendone')
    friend_two = models.ForeignKey(Shopper, related_name='friendtwo')
    created_at = models.DateTimeField('Friends Since', auto_now_add=True)

    @staticmethod
    def resolve_order(shopper_a, shopper_b):
        if shopper_a.pk < shopper_b.pk:
            friend_one, friend_two = shopper_a, shopper_b
        else:
            friend_one, friend_two = shopper_b, shopper_a
        return friend_one, friend_two

    @classmethod
    def add_friends(cls, shopper_a, shopper_b):
        friend_one, friend_two = Friend.resolve_order(shopper_a, shopper_b)
        friendship, created = cls.objects.get_or_create(friend_one=friend_one, friend_two=friend_two,
                                                        defaults=({'friend_one': friend_one, 'friend_two': friend_two}))
        return friendship

    @classmethod
    def remove_friends(cls, shopper_a, shopper_b):
        friend_one, friend_two = Friend.resolve_order(shopper_a, shopper_b)
        cls.objects.get(friend_one=friend_one, friend_two=friend_two).delete()

    @classmethod
    def is_friend(cls, shopper_a, shopper_b):
        friend_one, friend_two = Friend.resolve_order(shopper_a, shopper_b)
        return True if cls.objects.filter(friend_one=friend_one, friend_two=friend_two).count() else False

    @classmethod
    def get_friends(cls, shopper):
        friends = set([])
        friendships = cls.objects.filter(models.Q(friend_one=shopper) | models.Q(friend_two=shopper))
        for friendship in friendships:
            if friendship.friend_one == shopper:
                friends.add(friendship.friend_two)
            else:
                friends.add(friendship.friend_one)
        return friends


class Group(models.Model):
    user = models.ForeignKey(Shopper, related_name='groups')
    name = models.CharField(max_length=10)

    class Meta:
        unique_together = ("user", "name")

    @property
    def get_members(self):
        return [{'name': x.user.username, 'pk': x.user.pk} for x in self.groupmembers.all()]


class GroupMember(models.Model):
    user = models.ForeignKey(Shopper)
    group = models.ForeignKey(Group, related_name='groupmembers')


def create_shopper(sender, instance, **kwargs):
    if not Shopper.objects.filter(user=instance):
        Shopper.objects.create(user=instance)

post_save.connect(create_shopper, sender=User)




def friendify_all(sender, instance, **kwargs):
    """
    Makes everyone everyone's friend.
    """
    for shopper in Shopper.objects.all().exclude(pk=instance.pk):
        logger.info('Friending Up')
        shopper.add_friend(instance)

post_save.connect(friendify_all, sender=Shopper)
