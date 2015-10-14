__author__ = 'indrajit'


from django.db import models
from django.contrib.auth.models import User


CART_TYPES = (
    ('P', 'Personal'),
    ('S', 'Social'),
)

class Product(models.Model):
    pass

class Cart(models.Model):
    user = models.ForeignKey(SocialShopper, related_name='%(class)s')

    class Meta:
        abstract = True

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='%(class)s')
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField('Added At', auto_now_add=True)
    updated_at = models.DateTimeField('Updated At', auto_now_add=True)

    class Meta:
        abstract = True

class PersonalCart(Cart):
    pass

class PersonalCartItem(CartItem):
    pass

class SocialCart(Cart):
    uuid = models.UUIDField()
    is_active = models.BooleanField(default=True)

class SocialCartItem(CartItem):
    added_by = models.ForeignKey(SocialShopper)


class SocialShopper(models.Model):
    user = models.ForeignKey(User)

    def is_friends(self, friend):
        return SocialFriends.is_friend(self, friend)

    def add_friend(self, friend):
        return SocialFriends.add_friends(self, friend)

    def remove_friend(self, fried):
        return SocialFriends.remove_friends(self, fried)

class SocialFriends(models.Model):
    friend_one = models.ForeignKey(SocialShopper)
    friend_two = models.ForeignKey(SocialShopper)
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
        friend_one, friend_two = SocialFriends.resolve_order(shopper_a, shopper_b)
        return cls.objects.get_or_create(friend_one, friend_two)

    @classmethod
    def remove_friends(cls, shopper_a, shopper_b):
        friend_one, friend_two = SocialFriends.resolve_order(shopper_a, shopper_b)
        cls.objects.get(friend_one=friend_one, friend_two=friend_two).delete()

    @classmethod
    def is_friend(cls, shopper_a, shopper_b):
        friend_one, friend_two = SocialFriends.resolve_order(shopper_a, shopper_b)
        return True if cls.object.filter(friend_one, friend_two).count() else False


class SocialGroup(models.Model):
    user = models.ForeignKey(SocialShopper, related_name='groups')
    name = models.CharField(max_length=10)

    @property
    def get_members(self):
        return [{'name': x.user.username, 'pk': x.user.pk} for x in self.groupmembers]

class SocialGroupMember(models.Model):
    group = models.ForeignKey(SocialGroup, related_name='groupmembers')
    user = models.ForeignKey(SocialShopper)