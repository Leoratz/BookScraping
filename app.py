from bs4 import BeautifulSoup
import requests
import csv
import os
import pathlib
import re

### Site URL ###
url = "https://books.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

### Links and paths ###
path = pathlib.Path(__file__).parent.absolute()

os.makedirs(path / 'csv', exist_ok=True)
csv_file_path = path / 'csv' / 'books.csv'

os.makedirs(path / 'images', exist_ok=True)
image_path = path / 'images'

### Functions ###

def oneBook(book_url):
    sub_response = requests.get(book_url)
    sub_soup = BeautifulSoup(sub_response.content, 'html.parser')

    ### UPC ####
    upc = sub_soup.find_all('td')[0].text

    #### Title ####
    title = sub_soup.find('h1').text

    #### PIT ####
    pit = sub_soup.find_all('td')[3].text.replace('Â', '')

    #### PET ####
    pet = sub_soup.find_all('td')[2].text.replace('Â', '')

    #### NA ####
    div = soup.find('div', class_="product_price")

    if "In stock" in div.find_all('p')[1].text:
        na = re.findall(r'\d+', sub_soup.find_all('td')[5].text)[0]
    else:
        na = "Out of stock"

    #### PD ####
    pd = sub_soup.find('article', class_="product_page")
    description = pd.find_all('p')[3].text.replace(',', '')

    #### Category ####
    categories = sub_soup.find('ul', class_="breadcrumb")
    category = sub_soup.find_all('a')[3].text

    #### Rating ####
    stars = sub_soup.find('p', class_="star-rating")['class'][1]

    #### Image URL ####
    image = sub_soup.find('div', class_="item active")
    image_url = image.find('img')['src'].replace('../../', '')
    image_url = url + image_url

    try:
        getImage(image_url, title)
    except OSError or FileNotFoundError:
        book_title = title.replace(':', ' ').replace('/', ' ')
        getImage(image_url, book_title)
    

    return [book_url, upc, title, pit, pet, na, description, category, stars, image_url]

def getBooks(category_url):
    sub2_response = requests.get(category_url)
    sub2_soup = BeautifulSoup(sub2_response.content, 'html.parser')

    category = categories[20].find('a')['href']
    category_url = url + category

    books = sub2_soup.find_all('div', class_='image_container')
    for book in books:
        link = book.find('a')['href'].replace('../../../', 'catalogue/')
        book_url = url + link
        writer.writerow(oneBook(book_url))

    ### Exception for multiple pages ###
    next = sub2_soup.find('li', class_='next')
    if next:
        next_url = category_url + next.find('a')['href']
        pages_url = next_url.replace('index.html', '')
        getBooks(pages_url)

def getImage(book_url, title):
    image = requests.get(book_url)
    with open(image_path / f'{title}.jpg', 'wb') as file:
        file.write(image.content)


with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['product_page_url', 'universal_product_code ', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'])

    books = soup.find_all('div', class_='image_container')
    categories = soup.find_all('li')

    ### Product page URL ###
    link = books[0].find('a')['href']
    book_url = url + link

    ### Category URL ### 
    category = categories[20].find('a')['href']
    category_url = url + category

    getBooks(category_url)
