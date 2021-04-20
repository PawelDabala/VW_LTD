from bs4 import BeautifulSoup
from requests import get
import pprint


class VW_LCV:
    def __init__(self):
        page = get('https://vwdostawcze-sklep.pl')
        self.bs = BeautifulSoup(page.content, "html.parser")

        self.set_spider(self.bs)

    def set_spider(self, bs):
        categories = self.get_category_list(bs)

    def get_category_list(self, bs):
        category_links = bs.find('ul', class_="category-list swiper-wrapper").find_all("a")
        categories = []
        for category_link in category_links:
            categories.append({'link': category_link['href'],
                               'text': category_link.get_text("|", strip=True)
                               })
        return categories


VW_LCV()