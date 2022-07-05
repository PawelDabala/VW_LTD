from bs4 import BeautifulSoup
from requests import get
from pprint import pprint
from product_search import FindProduct


class Product:
    def __init__(self, product_name, products, path, page_address, products_category, tshirt = True):
        self.product_name = product_name
        self.products = products
        self.product = {}
        self.tshirt = tshirt

        product_category = self.get_product_category(products_category, products[-1])

        bs = self.get_page(path=path)
        self.set_product(bs=bs, page_address=page_address, path=path, product_category=product_category)

    def get_page(self, path):
        page = get(path)
        bs = BeautifulSoup(page.content, "html.parser")
        return bs

    def get_product_category(self, products_category, product_name):
        product_category = {}
        find_product = FindProduct(products_category)
        find_product.get_product(product_name)

        product_category['nr'] = find_product.get_google_nr()
        product_category['last_category'] = find_product.get_last_category_google()
        product_category['path'] = find_product.get_fb_product_path()
        return product_category

    def set_product(self, bs, page_address, path, product_category):
        self.product['main_category'] = self.product_name
        self.product['sub_name'] = self.products[-1]
        self.product['subproducts'] = self.products
        self.product['id'] = bs.find('span', class_='product__desc-number--bold').get_text()
        self.product['price'] = self.get_price(bs)
        self.product['weight'] = bs.find('p', class_='product__availability-item').find('span').get_text()
        self.product['availability'] = self.get_availability(bs)
        self.product['expected_availability'] = bs.find_all('p', class_="product__availability-item")[2].get_text("|",
                                                                                                                  strip=True)
        self.product['images'] = self.get_image(bs, page_address)
        self.product['description'] = self.get_description(bs)
        self.product['condition'] = 'New'
        self.product['link'] = path
        self.product['image_link'] = self.get_first_image_link(links_images=self.product['images'])
        self.product['brand'] = 'VW'
        self.product['additional_image_link'] = self.additional_image_link(links_images=self.product['images'])
        # fb SPRZĘT IT > Napędy optyczne
        self.product['google_product_category'] = product_category['path']
        self.product['sipping'] = 'PL:::15.00 PLN'
        self.product['google_product_category_nr'] = product_category['nr']
        # gg pralki-i-suszarki
        self.product['custom_label_0'] = product_category['last_category'].replace(' ', '-') if product_category['last_category'] is not None else None
        self.product['availability_'] = self.product['availability'].replace(' ', '_')

        if self.tshirt:
            self.product['tshirt_links'] = self.get_tshirt_size(bs)

        #check is bs
    def get_availability(self, bs):
        availability = bs.find_all('p', class_='product__availability-item')[1].find('span').get_text()
        return 'out of stock' if availability == 'Nie' else 'in stock'

    def get_image(self, bs, page_address):
        images = bs.find('div', class_='swiper-wrapper').find_all('img')
        return [page_address + image['src'] for image in images]

    def get_description(self, bs):
        description = bs.find('div', class_='product__txt-desc').get_text("|", strip=True)
        return description.replace('\xa0', '')

    def get_price(self, bs):
        text = bs.find('p', class_='price-vs').get_text()
        text = text.replace('PLN', '').replace(' ', '')
        return text + '.00 PLN'

    def get_first_image_link(self, links_images: list):
        return links_images[0] if len(links_images) > 0 else ''

    def additional_image_link(self, links_images: list):
        return ','.join(links_images[1:]) if len(links_images) >= 2 else ''

    def get_product(self):
        pprint(self.product)
        return self.product

    def get_tshirt_size(self, bs) -> list:
        """
        Get all links to tshirt size products
        """
        product_list = bs.find('div', class_ = 'product__size-list')
        if product_list is not None:
            tshirts_links = [tshirt['href'] for tshirt in product_list.find_all('a') ]
            return tshirts_links
        else:
            return None


if __name__ == '__main__':
    product = Product(product_name='CADDY 5',
                      products=['BAGAŻNIKI', 'BAGAŻNIKI DACHOWE',
                                'Belki bagażnika dachowego VW Caddy 5, do montażu na relingach, 2 szt.'],
                      path='https://vwdostawcze-sklep.pl/katalog/1/belki-bagaznika-dachowego-vw-caddy-544-do-montazu-na-relingach44-2-szt46,208403.html',
                      )
