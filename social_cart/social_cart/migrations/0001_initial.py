# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=2, choices=[(b'P', b'Personal'), (b'S', b'Social')])),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='CartInvite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField()),
                ('cart', models.ForeignKey(to='social_cart.Cart')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_id', models.BigIntegerField()),
                ('quantity', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'Added At')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name=b'Updated At')),
            ],
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'Friends Since')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='GroupMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group', models.ForeignKey(related_name='groupmembers', to='social_cart.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('item_id', models.BigIntegerField(unique=True)),
                ('msrp', models.FloatField()),
                ('sale_price', models.FloatField()),
                ('upc', models.BigIntegerField()),
                ('shortDescription', models.CharField(max_length=500)),
                ('url', models.URLField()),
                ('image_url', models.URLField()),
                ('brand_name', models.CharField(max_length=100)),
                ('rating', models.FloatField()),
                ('rating_url', models.URLField()),
                ('stock', models.CharField(max_length=20)),
                ('reviews', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Shopper',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='groupmember',
            name='user',
            field=models.ForeignKey(to='social_cart.Shopper'),
        ),
        migrations.AddField(
            model_name='group',
            name='user',
            field=models.ForeignKey(related_name='groups', to='social_cart.Shopper'),
        ),
        migrations.AddField(
            model_name='friend',
            name='friend_one',
            field=models.ForeignKey(related_name='friendone', to='social_cart.Shopper'),
        ),
        migrations.AddField(
            model_name='friend',
            name='friend_two',
            field=models.ForeignKey(related_name='friendtwo', to='social_cart.Shopper'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='added_by',
            field=models.ForeignKey(to='social_cart.Shopper'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(related_name='cartitems', to='social_cart.Cart'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(to='social_cart.Product'),
        ),
        migrations.AddField(
            model_name='cartinvite',
            name='invitee',
            field=models.ForeignKey(related_name='invitees', to='social_cart.Shopper'),
        ),
        migrations.AddField(
            model_name='cartinvite',
            name='owner',
            field=models.ForeignKey(related_name='owner', to='social_cart.Shopper'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(related_name='carts', to='social_cart.Shopper'),
        ),
    ]
