__author__ = 'indrajit'

import requests
import json

from django.core.management.base import BaseCommand, CommandError

from social_cart.settings import WALMART_API_KEY
from social_cart.models import Product, logger

class Command(BaseCommand):

    def handle(self, *args, **options):
        electronics_url = 'http://api.walmartlabs.com/v1/paginated/items?category=3944&specialOffer=rollback&apiKey={}&format=json'.format(WALMART_API_KEY)
        r = requests.get(electronics_url)
        response = json.loads(r.content)

        for product in response['items']:
            try:
                product_dict = {
                    'name': product['name'],
                    'item_id': product['itemId'],
                    'msrp': product['msrp'],
                    'sale_price': product['salePrice'],
                    'upc': product['upc'],
                    'url': product['productUrl'],
                    'image_url': product['thumbnailImage'],
                    'brand_name': product['brandName'],
                    'rating': product['customerRating'],
                    'rating_url': product['customerRatingImage'],
                    'reviews': product['numReviews'],
                    'stock': product['stock'],
                }
                Product.objects.get_or_create(item_id=product['itemId'], defaults=product_dict)
            except KeyError as e:
                logger.info(e)
                continue