import streamlit as sl
from scraping_functions import *

import os.path
from os import path

sl.title('LAPL Book Status')

if path.exists("bookinfo.csv"):
	book_pd = pd.read_csv("bookinfo.csv")

	is_available = sl.checkbox('Only show available books',value = True)

	if is_available:
		book_pd = book_pd[book_pd['Availability'] == 'On Shelf']

	is_circ = sl.checkbox('Only show books in circulation',value = True)
	if is_circ:
		book_pd = book_pd[book_pd['Location'] == 'CIRC']

	is_unique = sl.checkbox('Hide duplicates',value = True)
	if is_unique:
		book_pd = book_pd.drop_duplicates()

	sl.subheader('Branches')
	is_central = sl.checkbox('Central Library')
	if is_central:
		book_pd = book_pd[book_pd['Library'].str.contains('Central Library')]


	book_pd = book_pd.sort_values(by=['Library'])
	

	book_pd

else:
	sl.write('ERROR: bookinfo.csv file not found!')