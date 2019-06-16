import requests
from scraper.models import *
from market.models import *
from django.core.management.base import BaseCommand

import random
requests.packages.urllib3.disable_warnings()


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        items = Item.objects.all()
        stores = Store.objects.all()

        urls = {
            1: "https://vsemsmart.ru/index.php?route=product/product&product_id=16532",
            2: "http://e-mobi.com.ru/product.php?pr=16965",
            3: "https://calls.su/catalog/smartfony_i_smart_chasy/sredstva_svyazi/smartfony/5_84_smartfon_honor_10_128_gb_zelenyy/",
            4: "https://dnr-market.ru/telefony-i-svyaz/xiaomi/xiaomi-redmi-6-3-64gb-black-global-version",
            5: "http://tehnoland.shop/product.php?id=111580",
        }

        for item in items:
            mainPrice = random.randint(10000, 50000)

            for store in stores:
                dif = random.randint(500, 2500)
                corPrice = (mainPrice + dif) / 100 * 100
                print(f"{item.title} - {store.name}, {corPrice}")
                storeItem = StoreItem(store=store, item=item, price=corPrice, url=urls[store.id])
                storeItem.save()