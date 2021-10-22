## DB 
import psycopg2
## ENV
import os
from dotenv import load_dotenv
load_dotenv()
#SCRAPING
import requests
from bs4 import BeautifulSoup


#Create a connection credentials to the PostgreSQL database
try:
    connection = psycopg2.connect(
        user=os.getenv('DB_USER'), #"flapo"
        password=os.getenv('DB_PASSWORD'),  # "flapo",
        host=os.getenv('DB_HOST'),  # "localhost",
        port=os.getenv('DB_PORT'),  # "5432",
        database=os.getenv('DB_DATABASE'),  # "flapo_scraper"
    )

    print("You are connected into the database \n")
#Handle the error throws by the command that is useful when using python while working with PostgreSQL
except(Exception, psycopg2.Error) as error:
    print("Error connecting to PostgreSQL database", error)
    connection = None

# base_url = os.getenv('INDEED_BASE_URL') #'https: // de.indeed.com'
# review_url = os.getenv('INDEED_REVIEW_URL') #'https://de.indeed.com/cmp/Flaschenpost-Se/reviews'

# has_next_page = True

# while has_next_page:
#     review_page = requests.get(review_url)

#     soup = BeautifulSoup(review_page.content, 'html.parser')
#     review_container = soup.find(class_ = 'cmp-ReviewsList')

#     indeed_reviews = review_container.find_all(itemprop='review')

#     for indeed_review in indeed_reviews:
#         rating_element = indeed_review.select_one('button')
#         rating = float(rating_element.get_text())

#         review_title_element = indeed_review.find(attrs={"data-testid": "titleLink"})

#         review_detail_rel_link = review_title_element.attrs['href']
#         review_detail_link = base_url+review_detail_rel_link

#         title = review_title_element.contents[0].get_text()

#         author_element = indeed_review.find(itemprop='author')
#         date = author_element.contents[-1] # TODO Helper parse function

#         author_role = author_element.find_all('a')[0].get_text()

#         author_status = author_element.contents[-9] # TODO convert to bool

#         try:
#             author_location = author_element.find_all('a')[1].get_text()
#         except IndexError:
#             author_location = author_element.contents[-5]

#     # Check if next page exists
#     next_page_element = soup.find(title='Weiter')

#     if next_page_element is not None:
#         has_next_page = True
#         review_rel_url = next_page_element.attrs['href']
#         review_url = base_url + review_rel_url
#         print(review_rel_url)
#     else:
#         has_next_page = False
