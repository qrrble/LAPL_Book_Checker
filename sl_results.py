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

	# Checkboxes for filter for specific library branches
	is_central = sl.checkbox('Central Library',value = True)
	is_littletokyo = sl.checkbox('Little Tokyo',value = True)
	is_marvista = sl.checkbox('Mar Vista',value = True)
	is_palms = sl.checkbox('Palms-Rancho Park',value = True)

	branch_names = []

	if is_central:
		branch_names.append('Central Library')

	if is_littletokyo:
		branch_names.append('Little Tokyo Branch')

	if is_marvista:
		branch_names.append('Mar Vista Branch')

	if is_palms:
		branch_names.append('Palms-Rancho Park Branch')

	# Filters out library branches
	book_pd = book_pd[book_pd['Library'].str.contains('|'.join(branch_names))]

	book_pd = book_pd.sort_values(by=['Library'])
	
	book_pd

	if sl.button('Save filtered results to .csv'):
		book_pd[['Title','Library','Call_Number']].to_csv('lookup.csv',index=False)
		sl.write('Results saved to lookup.csv')


else:
	sl.write('ERROR: bookinfo.csv file not found!')