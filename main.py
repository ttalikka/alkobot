import json
import random
import requests
from bs4 import BeautifulSoup

# 103996 for Puolustuslaitos Leikattua, change for a different product
productCode = 103996

productUrl = "https://www.alko.fi/INTERSHOP/web/WFS/Alko-OnlineShop-Site/fi_FI/-/EUR/ViewProduct-Include?SKU={}".format(  # noqa
    str(productCode))
outletsUrl = "https://www.alko.fi/INTERSHOP/web/WFS/Alko-OnlineShop-Site/fi_FI/-/EUR/ALKO_ViewStoreLocator-StoresJSON"  # noqa


def get_data_from_url(url: str):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    content = json.loads(
        soup.find(attrs={"type": "application/json"}).contents[0])
    return content


def get_store_by_id(id: str):
    r = requests.get(outletsUrl)
    outlets = json.loads(r.text)
    for outlet in outlets["stores"]:
        if outlet["storeId"] == id:
            return outlet
    return None


availability = get_data_from_url(productUrl)
outlet = random.choice(availability)
outletData = get_store_by_id(outlet["storeId"])

print(
    "Leikattua on saatavilla {} pulloa myymälässä {}".format(
        outlet["stock"], outletData["name"]))

print("Kartalla: https://www.openstreetmap.org/#map=18/{}/{}".format(
    outletData["latitude"], outletData["longitude"]))
