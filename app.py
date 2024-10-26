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

### Paths ###
path = pathlib.Path(__file__).parent.absolute()
os.makedirs(path / 'csv', exist_ok=True)
os.makedirs(path / 'images', exist_ok=True)

### Functions ###

def oneBook(book_url):
    """
    Extract all informations about one book

    Args:
        book_url (str): URL of the book

    Returns:
        list: List of all informations about the book
    """

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

    getImage(image_url, title, category)
    
    return [book_url, upc, title, pit, pet, na, description, category, stars, image_url]

def getBooks(category_url, writer):
    """
    Extract all books from a category

    Args:
        category_url (str): URL of the category
        writer (csv.writer): CSV writer
    
    Returns:
        None
    """

    while category_url:
        sub2_response = requests.get(category_url)
        sub2_soup = BeautifulSoup(sub2_response.content, 'html.parser')

        books = sub2_soup.find_all('div', class_='image_container')
        for book in books:
            link = book.find('a')['href'].replace('../../../', 'catalogue/')
            book_url = url + link
            writer.writerow(oneBook(book_url))

        ### Exception for multiple pages ###
        next = sub2_soup.find('li', class_='next')
        if next:
            next_url = next.find('a')['href']
            category_url = category_url.rsplit('/', 1)[0] + '/' + next_url
            print(category_url)
        else:
            category_url = None

def getImage(book_url, title, category):
    """
    Get the image of a book

    Args:
        book_url (str): URL of the book
        title (str): Title of the book
        category (str): Category of the book

    Returns:
        None
    """

    valid_title = re.sub(r'[<>:"/\\|?*]', '_', title)

    category_path = path / 'images' / category
    os.makedirs(category_path, exist_ok=True)

    image = requests.get(book_url)
    with open(category_path / f'{valid_title}.jpg', 'wb') as file:
        file.write(image.content)


def getAllBooks():
    """
    Extract all books from the website

    Args:
        None
    
    Returns:
        None
    """

    categories = soup.find('ul', class_='nav nav-list').find('ul').find_all('li')
    
    for category in categories:
        category_name = category.find('a').text.strip()
        category_url = url + category.find('a')['href']
        print(category_url)

        csv_file_path = path / 'csv' / f'{category_name}.csv'
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['product_page_url', 'universal_product_code', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'])
            getBooks(category_url, writer)

### Main Execution ###
getAllBooks()