from bs4 import BeautifulSoup
from requests import get


class Product:
    def __init__(self, product_name, products, name, path):
        self.product_name = product_name
        self.products = products
        self.name = name
        self.path = path

    def get_data(self, path):

