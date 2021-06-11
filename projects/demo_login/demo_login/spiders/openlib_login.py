import scrapy
from scrapy import FormRequest

class OpenlibLoginSpider(scrapy.Spider):
    name = 'openlib_login'
    allowed_domains = ['openlibrary.org']
    start_urls = ['https://openlibrary.org/account/login']

    def parse(self, response):
        yield FormRequest.from_response(
            response,
            formid='register',
            formdata={
                'username': 'geoffrey.bulot@gmail.com',
                'password': 'l92Bo6NoXo',
                'redirect': 'https://openlibrary.org/',
                'debug_token': '',
                'login': 'Log In'
            },
            callback=self.after_login
        )

    def after_login(self, response):
        print('here we go logged in')