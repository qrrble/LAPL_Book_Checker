from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup, Tag
import requests
import pandas as pd

def GetBookCopyInfo(input_url):
    # Initializes Selenium driver
    driver = webdriver.PhantomJS()
    driver.get(input_url)

    delay = 5 # seconds

    # Scrapes the page, and waits until the content is fully loaded before proceeding
    try:
        elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'details_allCopiesContainer')))
        elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'detailsContainer')))
        source_code = elem.get_attribute("outerHTML")
        soup = BeautifulSoup(source_code, 'html.parser')
        content = soup.find('div',id = 'detailsContainer')
    except TimeoutException:
        return None
       
    book_title = content.find('h2').text
    book_author = content.find('h3').text[3:]

    library_branches = content.find_all('div',class_ = 'dataTable')

    book_copy_pd = pd.DataFrame(columns = ['Title','Author','Library', 'Location','Call_Number','Availability'])

    # Loops over all the library branches in the Copies table
    for x in library_branches:
        library_name = x.find('a',target = '_blank').get_text()

        # Gets information for all of the copies in a given branch, and stores information into a list
        all_copies = x.find_all('tr',class_="odd") +x.find_all('tr',class_="even")
        
        for copy in all_copies:
            single_copy_info = [y.get_text() for y in copy.find_all('td')]
            location = single_copy_info[0]
            call_number = single_copy_info[1]
            availability = single_copy_info[2]
            
            book_copy_pd = book_copy_pd.append({'Title':book_title,'Author':book_author,'Library':library_name, 'Location':location,'Call_Number':call_number,'Availability':availability} , ignore_index=True)

    return book_title,book_author,book_copy_pd



def GetBookList(input_url):
    page = requests.get(input_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    items = soup.find_all('item')

    book_list_dict = {}
    book_list_pd = pd.DataFrame(columns = ['Title','URL','Thumbnail'])

    for x in items:
        # Book title
        title = x.find('title').get_text()
        
        # URL for book info
        copy_info_url = x.find('guid').get_text() + '&view=allCopiesDetailsTab'
        
        # Book thumbnail
        description = x.find('description')
        description_soup = BeautifulSoup(description.get_text(), 'html.parser')
        thumbnail_url = description_soup.find('img')['src']
        
        book_list_dict[title] = {'copy_info':copy_info_url, 'thumbnail':thumbnail_url}
        book_list_pd = book_list_pd.append({'Title':title,'URL':copy_info_url,'Thumbnail':thumbnail_url} , ignore_index=True)
        
    return book_list_pd