import streamlit as sl
from scraping_functions import *

sl.title('LAPL Book List')

book_list_url = 'https://ls2pac.lapl.org/list/static/1899001892/rss' # RSS link

input_url = sl.text_input('Enter a LAPL book list URL here',value = book_list_url)

book_list_pd = GetBookList(input_url)

for index,book in book_list_pd.iterrows():
    title = book['Title']
    url = book['URL']
    thumbnail = book['Thumbnail']
    sl.markdown("![%s](%s) [%s](%s)" % (title,thumbnail,title,url))
