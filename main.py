from bs4 import BeautifulSoup
from requests import get
import pprint


class VW_LCV:
    def __init__(self):
        page = get('https://vwdostawcze-sklep.pl')
        self.bs = BeautifulSoup(page, "html.parser")

        self.set_category(self.bs)

    def set_category(self, bs):
        category_list = self.get_category_list(bs)

    def get_category_list(self, bs):
        pass