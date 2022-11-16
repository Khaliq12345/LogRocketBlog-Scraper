import scrapy
from ..items import LogrocketblogScraperItem

class Logrocket_Spider(scrapy.Spider):
    page_number = 2
    name = 'Logrocketblog'
    start_urls = ['https://blog.logrocket.com/page/1/']

    def parse(self, response):
        items = LogrocketblogScraperItem()

        blogs = response.css('.highlighted')
        for blog in blogs:
            title = blog.css('.card-title a::text').extract_first()
            about = blog.css('.d-block::text').extract_first()
            author = blog.css('.post-name a::text').extract_first()
            date = blog.css('.post-date::text').extract_first()
            readTime = blog.css('.readingtime::text').extract_first()
            link = blog.css('.thumbimage::attr(href)').get()

            items['title'] = title
            items['about'] = about
            items['author'] = author
            items['date'] = date
            items['readTime'] = readTime
            items['link'] = link

            yield items

        next_page = f'https://blog.logrocket.com/page/{Logrocket_Spider.page_number}/'
        Logrocket_Spider.page_number += 1

        if Logrocket_Spider.page_number < 283:
            yield response.follow(next_page, callback = self.parse)