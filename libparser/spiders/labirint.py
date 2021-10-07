import scrapy


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D0%BF%D1%80%D0%B8%D0%BA%D0%BB%D1%8E%D1%87%D0%B5%D0%BD%D0%B8%D1%8F/?order=relevance&way=back&stype=0&paperbooks=1&ebooks=1&otherbooks=1&available=1&preorder=1&wait=1&no=1&price_min=3&price_max=150',
                  'https://www.labirint.ru/search/%D0%BF%D1%80%D0%B8%D0%BA%D0%BB%D1%8E%D1%87%D0%B5%D0%BD%D0%B8%D1%8F/?order=relevance&way=back&stype=0&paperbooks=1&ebooks=1&otherbooks=1&available=1&preorder=1&wait=1&no=1&price_min=151&price_max=300']

    def parse(self, response: HtmlResponse):
        base_url = 'https://www.labirint.ru'
        relative_links = response.xpath('//a[@class="product-title-link"]/@href').getall()
        links = [f'{base_url}{link}' for link in relative_links]
        next_page = response.xpath('//a[@title="Следующая"]/@href').get()

        if next_page:
            yield response.follow(next_page, callback=self.parse)

        for link in links:
            yield response.follow(link, callback=self.parse_book)
        print(response.url)


    def parse_book(self, response: HtmlResponse):
        url = response.url
        name = response.xpath('//h1/text()').get()
        author = response.xpath('//a[@data-event-label="author"]/text()').get()
        price_with_no_discount = response.xpath('//span[@class="buying-priceold-val-number"]/text()').get()
        price = response.xpath('//span[@class="buying-pricenew-val-number"]/text()').get()
        rating = response.xpath('//div[@id="rate"]/text()').get()
        yield LibparserItem(url=url,
                             name=name, author=author,
                             price_with_no_discount=price_with_no_discount,
                             price=price,
                             rating=rating)
