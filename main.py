from bs4 import BeautifulSoup
from requests import get
import pprint


class VW_LCV:
    page_address = 'https://vwdostawcze-sklep.pl'

    def __init__(self):
        page = get(self.page_address)
        self.bs = BeautifulSoup(page.content, "html.parser")

        self.set_spider(self.bs)
        self.final_data = []

    def set_spider(self, bs):
        categories = self.get_category_list(bs)
        self.get_subcategoires(bs, categories)

    def get_category_list(self, bs):
        category_links = bs.find('ul', class_="category-list swiper-wrapper").find_all("a")
        categories = []
        for category_link in category_links:
            categories.append({'link': category_link['href'],
                               'name': category_link.get_text("|", strip=True)
                               })
        return categories

    def get_subcategoires(self, bs, categories):
        """
        Get subproducts for each category"
        """

        for category in categories:
            subproduct_address = self.page_address + category['link']
            subproducts_page = get(subproduct_address)
            bs_subproducts_list = BeautifulSoup(subproducts_page.content, "html.parser")
            self.get_products(bs_subproducts_list, category['name'])

    def get_products(self, subproducts, name):

        finish = True
        nr = 0
        products = []
        while finish and nr <= 5:
            # todo function to check all records have status finish
            if len(products) == 0:
                # make new dictinary
                alists = subproducts.find_all('a', class_="product-list__item")
                price = True if alists[0].find("div", class_="product-list__price") else False
                if price:
                    # "no more subcategories"
                    for alist in alists:
                        products.append({'product_name': name,
                                         'products': [f'{alist.find("p").get_text()}'],
                                         'path': alist['href'],
                                         'finish': True
                                         })
                    finish = True
                else:
                    for alist in alists:
                        products.append({'product_name': name,
                                         'products': [f'{alist.find("p").get_text()}'],
                                         'path': alist['href'],
                                         'finish': False
                                         })
            else:
                # add product to key products
                temp_products = []
                for product in products:
                    path = get(self.page_address + product['path'])
                    products_bs = BeautifulSoup(path.content, "html.parser")
                    alists = products_bs.find_all('a', class_="product-list__item")
                    price = True if alists[0].find("div", class_="product-list__price") else False

                    if price:
                        # "no more subcategories"
                        # do zmiany produkt powinien dodawać się do nowej zmiennej
                        for alist in alists:
                            product['products'].append(f'{alist.find("p").get_text()}')
                            product['path'] = alist['href']
                            product['finish'] = True
                            temp_products.append(product)
                        finish = True
                    else:
                        for alist in alists:
                            product['products'].append(f'{alist.find("p").get_text()}')
                            product['path'] = alist['href']
                            product['finish'] = False
                            temp_products.append(product)

                products = temp_products
            print(nr)
            nr += 1


VW_LCV()
