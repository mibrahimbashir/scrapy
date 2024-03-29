import scrapy
from bookscraper.items import BookItem


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    custom_settings = {
        "FEEDS": {
            "booksdata.json": {
                "format": "json",
                "overwrite": True
            }
        }
    }

    def parse(self, response):
        books = response.css("article.product_pod")

        for book in books:
            book_relative_url = book.css("h3 a ::attr(href)").get()

            if "catalogue/" in book_relative_url:
                book_url = "http://books.toscrape.com/" + book_relative_url
            else:
                book_url = "http://books.toscrape.com/catalogue/" + book_relative_url

            yield response.follow(book_url, callback=self.parse_book)

        next_page_relative_url = response.css("li.next a ::attr(href)").get()

        if next_page_relative_url is not None:
            if "catalogue/" in next_page_relative_url:
                next_page_url = "http://books.toscrape.com/" + next_page_relative_url
            else:
                next_page_url = "http://books.toscrape.com/catalogue/" + next_page_relative_url

            yield response.follow(next_page_url, callback=self.parse)

    def parse_book(self, response):
        book = BookItem()
        table_rows = response.css("table tr")

        book['url'] = response.url
        book['upc'] = table_rows[0].css("td ::text").get()
        book['product_type'] = table_rows[1].css("td ::text").get()
        book['price_excl_tax'] = table_rows[2].css("td ::text").get()
        book['price_incl_tax'] = table_rows[3].css("td ::text").get()
        book['tax'] = table_rows[4].css("td ::text").get()
        book['availability'] = table_rows[5].css("td ::text").get()
        book['reviews'] = table_rows[6].css("td ::text").get()
        book['description'] = response.xpath("//div[@id='product_description']/following-sibling::p/text()").get()
        book['genre'] = response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get()
        book['price'] = response.css("div.product_main p.price_color ::text").get()
        book['stars'] = response.css("div.product_main p.star-rating ::attr(class)").get()

        yield book
