import scrapy


class GlassesSpider(scrapy.Spider):
    name = 'glasses'
    allowed_domains = ['www.glassesshop.com']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    start_urls = ['http://www.glassesshop.com/bestsellers/']

    # def start_requests(self):
    #     yield scrapy.Request(url='https://www.glassesshop.com/bestsellers', callback=self.parse, headers={
    #         'User-Agent': self.user_agent
    #     })

    def parse(self, response):
        # debugging: inspect parse response
        # inspect_parse(response, self) (import from scrapy shell)
        glasses = response.xpath("//div[@id='product-lists']/div")
        for product in glasses:
            title = product.xpath("normalize-space(.//div[@class='p-title']/a/text())").get()
            if not title == "":
                yield {
                    'title': product.xpath("normalize-space(.//div[@class='p-title']/a/text())").get(),
                    'price': product.xpath(".//div[@class='p-price']//span/text()").get(),
                    'img': product.xpath(".//img[@class='lazy d-block w-100 product-img-default']/@data-src").get(),
                    # 'User-Agent': response.request.headers['User-Agent']
                }

        # pagination handling
        next_page = response.xpath("//ul[@class='pagination']/li[position() = last()]/a/@href").get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
