from bs4 import BeautifulSoup
from requests import get


class Product:
    def __init__(self, product_name, products,  path):
        self.product_name = product_name
        self.products = products

        bs = self.get_page(path=path)
        self.set_product(bs=bs)

    def get_page(self, path):
        page = get(path)
        bs = BeautifulSoup(page.content, "html.parser")
        return bs

    def set_product(self, bs):
        product ={}
        product['name'] = self.product_name
        product['id'] = bs.find('span', class_='product__desc-number--bold').get_text()
        product['price'] = bs.find('p', class_='price-vs').get_text()
        product['weight'] = bs.find('p', class_='product__availability-item').find('span').get_text()
        product['availability'] = self.get_availability(bs)
        

        pass

    def get_availability(self, bs):
        availability = bs.find_all('p', class_ ='product__availability-item')[1].find('span').get_text()
        return 'No' if availability == 'Nie' else 'Yes'





if __name__ == '__main__':
    product = Product(product_name='CADDY 5',
                      products=['BAGAŻNIKI', 'BAGAŻNIKI DACHOWE',
                                'Belki bagażnika dachowego VW Caddy 5, do montażu na relingach, 2 szt.'],
                      path='https://vwdostawcze-sklep.pl/katalog/1/belki-bagaznika-dachowego-vw-caddy-544-do-montazu-na-relingach44-2-szt46,208403.html',
                      )
