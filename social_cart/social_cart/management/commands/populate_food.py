__author__ = 'indrajit'

import requests
import json

from django.core.management.base import BaseCommand, CommandError

from social_cart.settings import WALMART_API_KEY
from social_cart.models import Product, logger

class Command(BaseCommand):

    def handle(self, *args, **options):
        category_list = ['976759_1071964_976779', '976759_976788_1001466', '976759_976782_1001319', '976759_976788', '2636_1224908_1224996']
        for category_id in category_list:
            try:
                url = 'http://api.walmartlabs.com/v1/paginated/items?category={}&apiKey={}&format=json'.format(category_id, WALMART_API_KEY)
                r = requests.get(url)
                response = json.loads(r.content)
                for product in response['items'][:4]:  # Don't want more than 10 per category
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
            except Exception as e:
                logger.exception(e)
                continue
