import scrapy
import datetime
import os
from dotenv import load_dotenv
load_dotenv()

class PostSpider(scrapy.Spider):
  name = "indeed"
  start_urls = [
      'https://de.indeed.com/cmp/Flaschenpost-Se/reviews?start=0'
  ]

  def parse(self, response):
    
    base_url = os.getenv('INDEED_BASE_URL')
    reviews = response.css('div[itemprop="review"]')

    def parse_month_string(month_string):
      if month_string == 'Januar':
          return 1
      elif month_string == 'Februar':
          return 2
      elif month_string == 'März':
          return 3
      elif month_string == 'April':
          return 4
      elif month_string == 'Mai':
          return 5
      elif month_string == 'Juni':
          return 6
      elif month_string == 'Juli':
          return 7
      elif month_string == 'August':
          return 8
      elif month_string == 'September':
          return 9
      elif month_string == 'Oktober':
          return 10
      elif month_string == 'November':
          return 11
      elif month_string == 'Dezember':
          return 12
      else:
          raise TypeError(f"No matching month: {month_string}")

    def parse_date_string(date_string):
      date_string_split = date_string.split(' ')

      day = int(date_string_split[0].replace('.', ''))
      month = parse_month_string(date_string_split[1])
      year = int(date_string_split[2])

      date = datetime.date(year, month, day)
      return date

    def parse_author_status(status_string):
        if status_string == '(Ehemaliger Mitarbeiter)':
            return False
        elif status_string == '(Derzeitiger Mitarbeiter)':
            return True
        else:
            return None

    for review in reviews:
      yield {
          'title': review.css('a[data-testid="titleLink"] span span span::text').get(),
          'url': base_url + review.css('a[data-testid="titleLink"]::attr(href)').get(),
          'creation_date': parse_date_string(review.css('span[itemprop="author"]::text').getall()[-1]),
          'total_rating_score': review.css('meta[itemprop="ratingValue"]::attr(content)').get(),
          'author_status': parse_author_status(review.css('span[itemprop="author"]::text').getall()[1]),
          'author_role': review.css('span[itemprop="author"] a::text').get(),
          'author_location': review.css('span[itemprop="author"] a[href*=fcountry]::text').get(),
      }

    next_page = response.css('a[data-tn-element="next-page"]::attr(href)').get()
    if next_page is not None:
      next_page = response.urljoin(next_page)
      yield scrapy.Request(next_page, callback=self.parse)
      
