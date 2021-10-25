# ENV
import os
from dotenv import load_dotenv
load_dotenv()

# SCRAPING
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

from scraping.models import Review, Platform
import datetime
import time
import chromedriver_binary

# AUTOMATION
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Collect review from Indeed"

    def handle(self, *args, **options):

      platform, created = Platform.objects.get_or_create(
          title='Glassdoor',
          defaults={'last_scraped': None}
      )

      base_url = os.getenv('GLASSDOOR_BASE_URL')  # 'https://www.glassdoor.de/'
      review_url = os.getenv('GLASSDOOR_REVIEW_URL')
      # 'https://www.glassdoor.de/Bewertungen/flaschenpost-Bewertungen-E0606852.htm?sort.sortType=RD&sort.ascending=false&filter.iso3Language=deu'

      GOOGLE_CHROME_PATH = os.getenv('GOOGLE_CHROME_PATH')
      CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH')

      options = webdriver.ChromeOptions()
      options.headless = True
      options.add_argument('--disable-gpu')
      options.add_argument('--no-sandbox')
      options.add_argument('--remote-debugging-port=9222')
      options.binary_location = GOOGLE_CHROME_PATH

      driver = webdriver.Chrome(
          executable_path=CHROMEDRIVER_PATH, chrome_options=options)
      
      # For local development
      # driver = webdriver.Chrome(chrome_options=options)

      driver.get(review_url)

      element = WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.ID, "ReviewsFeed"))
      )

      # driver.execute_script(
      #     "document.getElementById('onetrust-consent-sdk').style.display='none';")

      has_next_page = True
      new_review_count = 0
      page = 1

      while has_next_page:
          review_container = driver.find_element(By.ID, 'ReviewsFeed')
          glassdoor_reviews = review_container.find_elements(By.CLASS_NAME, 'empReview')

          for review in glassdoor_reviews:
              rating_element = review.find_element(By.CLASS_NAME, 'ratingNumber')
              rating = float(rating_element.text.replace(',', '.'))

              review_title_element = review.find_element(By.CLASS_NAME, 'reviewLink')


              review_detail_rel_link = review_title_element.get_attribute('href')
              review_detail_link = base_url+review_detail_rel_link

              title = review_title_element.text
              
              # Expanding further categories if available
              # try:
              #   expand_button = review.find_element(
              #       By.CLASS_NAME, 'v2__EIReviewDetailsV2__continueReading')#.click()
              #   driver.execute_script("arguments[0].click();", expand_button)
              #   time.sleep(.2)
              # except Exception as e:
              #   print('No Button')

              # Review body is split up into different categories that need to be merged together
              content = ''
              content_list = review.find_elements(By.CLASS_NAME, 'v2__EIReviewDetailsV2__fullWidth')
              
              for content_piece in content_list:
                # Comment by the employer have same identifier, but dont contain strong tag
                try:
                  category = content_piece.find_element(By.CLASS_NAME, 'strong').text
                  body = content_piece.find_element(By.CLASS_NAME, 'v2__EIReviewDetailsV2__bodyColor').text
                  content = content + category + ': ' + body + '; '
                except NoSuchElementException:
                  pass


              # Author string contains Job Role and Creation Date
              author_string = review.find_element(By.CLASS_NAME, 'authorJobTitle').text
              
              try:
                author_string_split = author_string.split(' - ')
                date = author_string_split[0]
                author_role = author_string_split[1]
              except Exception as e:
                print(e)
              
              author_status = review.find_element(By.CLASS_NAME, 'pt-xsm').text # TODO find better identifier

              try:
                  author_location = review.find_element(
                      By.CLASS_NAME, 'authorLocation').text
              except NoSuchElementException:
                  author_location = 'NA'

              try:
                  # Try to create new or match with existing review based on review URL
                  review, created = Review.objects.update_or_create(
                      url=review_detail_link,
                      defaults={
                          'platform': platform,
                          'title': title,
                          'date': date,
                          'rating': rating,
                          'content': content,
                          'author_status': author_status,
                          'author_role': author_role,
                          'author_location': author_location
                      }
                  )

                  if created:
                    new_review_count = new_review_count + 1
              except Exception as e:
                print(e)

          # Check if next page exists, end scraping if last page was scraped
          next_page_button = driver.find_element(By.CLASS_NAME, 'nextButton')

          if next_page_button.is_enabled():
            has_next_page = True

            # New driver needed to bypass need for authentication
            page = page + 1
            next_page_link = f"https://www.glassdoor.de/Bewertungen/flaschenpost-Bewertungen-E2606852_P{str(page)}.htm?filter.iso3Language=deu"
            
            driver.quit()
            driver = webdriver.Chrome(options=options)
            driver.get(next_page_link)
            
            
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "ReviewsFeed"))
            )

            # driver.execute_script(
            #     "document.getElementById('onetrust-consent-sdk').style.display='none';")
          else:
            has_next_page = False
            driver.quit()

      platform.last_scraped = datetime.date.today()
      platform.save()

      self.stdout.write(f"Glassdoor review import complete. {new_review_count} new reviews added.")
