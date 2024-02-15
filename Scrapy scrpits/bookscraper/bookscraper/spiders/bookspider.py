import scrapy

class BookspiderSpider(scrapy.Spider):
    # Name of the spider
    name = "bookspider"

    # Spider will only look for URLs within this domain
    allowed_domains = ["books.toscrape.com"]

    # Spider will start crawling from this URL
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        # Extracting information about each book on the current page
        books = response.css('article.product_pod')

        for book in books:
            yield {
                'name': book.css('h3 a::text').get(),
                'price': book.css('.product_price .price_color::text').get(),
                'url': book.css('h3 a').attrib['href'],
            }

        # Extracting the URL of the next page
        next_page = response.css('li.next a ::attr(href)').get()

        if next_page is not None:
            # Checking if the URL is relative or absolute
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page

            # Following the link to the next page and calling the parse method recursively
            yield response.follow(next_page_url, callback=self.parse)
