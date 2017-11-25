import scrapy
from scrapy.selector import Selector
import re
from tutorial.items import ElradarItem

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext


class Elradar(scrapy.Spider):
    name = "ElradarNews"
    allowed_domains = ['elrdar.com']
    start_urls = ['https://www.elrdar.com/category/economy-news/page/1/']


    def parse(self, response):
        articles =response.xpath("//h2[contains(@class,'entry-title')]/a/@href").extract()
        if articles is None or len(articles) == 0:
            print "articles noooooooooooooooone"
        else:
            print "articles not nooooooooooooooooone"
            print len(articles)
        for article in articles:
            if article is not None:
                article = 'https://www.elrdar.com/' + article
                print "Next article is: "
                print article.encode('utf-8')
                yield scrapy.Request(article, callback=self.parse_page)
            else:
                print "Noneeeeeeeeeeeeeeeeee"

        next_page = response.xpath("//div/a[contains(@class, 'next page-numbers')]/@href").extract_first()
        if next_page is not None:
            #next_page = 'https://www.elrdar.com/' + next_page
            yield scrapy.Request(next_page, callback=self.parse)
        else:
            print response.url

    def parse_page(self, response):
        print "Ana gwa parse page"
        title = response.xpath("//div[contains(@class, 'container main')]/header/h1/text()").extract_first().encode('utf-8')
        body = ""
        date = response.xpath("//time[contains(@class,'entry-date published updated')]/@datetime").extract_first()[0:10]
        sel = Selector(response)
        paragraphs = sel.xpath("//div[contains(@class, 'contents entry-content')]/text()").extract()
        # for p in paragraphs:
        #     body = body + '\n' + p
        body = cleanhtml(paragraphs)
        link = response.url
        body.replace(","," ")

        yield ElradarItem(title=title, link=link, body=body, date=date)