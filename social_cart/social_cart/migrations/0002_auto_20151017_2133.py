# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_cart', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='item_id',
        ),
        migrations.AddField(
            model_name='shopper',
            name='gcm_key',
            field=models.CharField(max_length=400, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='cartinvite',
            name='cart',
            field=models.ForeignKey(related_name='cartinvitees', to='social_cart.Cart'),
        ),
    ]
