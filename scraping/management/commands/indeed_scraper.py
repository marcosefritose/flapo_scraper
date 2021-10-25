# ENV
import os
from dotenv import load_dotenv
load_dotenv()

# SCRAPING
import requests
import datetime
from bs4 import BeautifulSoup
from scraping.models import Review, Platform

# AUTOMATION
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Collect review from Indeed"

    def handle(self, *args, **options):
        platform, created = Platform.objects.get_or_create(
            title = 'Indeed',
            defaults={'last_scraped': None}
        )

        base_url = os.getenv('INDEED_BASE_URL') #'https: // de.indeed.com'
        review_url = os.getenv('INDEED_REVIEW_URL') #'https://de.indeed.com/cmp/Flaschenpost-Se/reviews'

        has_next_page = True
        new_review_count = 0

        while has_next_page:
            review_page = requests.get(review_url)

            soup = BeautifulSoup(review_page.content, 'html.parser')
            review_container = soup.find(class_ = 'cmp-ReviewsList')

            indeed_reviews = review_container.find_all(itemprop='review')

            for indeed_review in indeed_reviews:
                rating_element = indeed_review.select_one('button')
                rating = float(rating_element.get_text())

                review_title_element = indeed_review.find(attrs={"data-testid": "titleLink"})

                review_detail_rel_link = review_title_element.attrs['href']
                review_detail_link = base_url+review_detail_rel_link

                title = review_title_element.contents[0].get_text()
                content = indeed_review.find(itemprop='reviewBody').get_text()

                author_element = indeed_review.find(itemprop='author')
                date = author_element.contents[-1] # TODO Helper parse function

                author_role = author_element.find_all('a')[0].get_text()

                author_status = author_element.contents[-9] # TODO convert to bool

                try:
                    author_location = author_element.find_all('a')[1].get_text()
                except IndexError:
                    author_location = author_element.contents[-5]

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
                    print('Error saving Indeed Review! \n')
                    #print(e)

            # Check if next page exists, end scraping if last page was scraped
            next_page_element = soup.find(title='Weiter')

            if next_page_element is not None:
                has_next_page = True
                review_rel_url = next_page_element.attrs['href']
                review_url = base_url + review_rel_url
            else:
                has_next_page = False

        platform.last_scraped = datetime.date.today()
        platform.save()

        self.stdout.write(f"Indeed review import complete. {new_review_count} new reviews added.")
