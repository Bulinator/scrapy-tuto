import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']
    # start_urls = ['https://www.imdb.com/search/title/?groups=top_250&sort=user_rating']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'

    # no need to set callback method in start_requests method
    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/search/title/?groups=top_250&sort=user_rating', headers={
            'User-Agent': self.user_agent
        })

    rules = (
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']/a"), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="//a[@class='lister-page-next next-page'][1]"), process_request='set_user_agent')
    )

    # spider args is required
    def set_user_agent(self, request, spider):
        request.headers['User-agent'] = self.user_agent
        return request

    def parse_item(self, response):
        yield {
            'title': response.xpath("//div[@class='TitleBlock__TitleContainer-sc-1nlhx7j-1 jxsVNt']/h1/text()").get(),
            'year': response.xpath("//div[@class='TitleBlock__TitleMetaDataContainer-sc-1nlhx7j-4 cgfrOx']/ul/li/a/text()").get(),
            'duration': response.xpath("normalize-space(//div[@class='TitleBlock__TitleMetaDataContainer-sc-1nlhx7j-4 cgfrOx']/ul/li/text())").get(),
            'rating': response.xpath("//div[@class='AggregateRatingButton__Rating-sc-1il8omz-2 ckpPOV']/span/text()").get(),
            'genre': response.xpath("//div[@class='ipc-chip-list ipc-chip-list--wrap GenresAndPlot__GenresChipList-cum89p-6 fLrtBh']/a/span/text()").getall(),
            'movie_url': response.url,
            # 'user-agent': response.request.headers['User-Agent']
        }
