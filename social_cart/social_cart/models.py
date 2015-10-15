__author__ = 'indrajit'


from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


CART_TYPES = (
    ('P', 'Personal'),
    ('S', 'Social'),
)


class Shopper(models.Model):
    user = models.ForeignKey(User)

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


class Product(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    image_url = models.URLField()


class Cart(models.Model):
    user = models.ForeignKey(Shopper, related_name='%(class)s')
    type = models.CharField(choices=CART_TYPES, max_length=2)
    uuid = models.UUIDField()
    is_active = models.BooleanField(default=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='%(class)s')
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField('Added At', auto_now_add=True)
    updated_at = models.DateTimeField('Updated At', auto_now_add=True)
    added_by = models.ForeignKey(Shopper)

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
        return True if cls.object.filter(friend_one, friend_two).count() else False

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

    @property
    def get_members(self):
        return [{'name': x.user.username, 'pk': x.user.pk} for x in self.groupmembers]


class GroupMember(models.Model):
    user = models.ForeignKey(Shopper)
    group = models.ForeignKey(Group, related_name='groupmembers')


def create_shopper(sender, instance, **kwargs):
    if not Shopper.objects.filter(user=instance):
        Shopper.objects.create(user=instance)

post_save.connect(create_shopper, sender=User)
