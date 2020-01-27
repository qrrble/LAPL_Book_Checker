import streamlit as sl
from scraping_functions import *

sl.title('LAPL Book Availability Checker')
sl.write('Check the availability and status of books in a LAPL book list.')

book_list_url = 'https://ls2pac.lapl.org/list/static/1899001892/rss' # RSS link
input_url = sl.text_input('Enter a LAPL book list URL here',value = book_list_url)

# Gets book list data
book_list_pd = GetBookList(input_url)

sl.write('Books to query:')
book_list_pd['Title']

is_save_csv = sl.checkbox('Save results to .csv file') 

# Checks availability data
if sl.button('Check availability!'):
	# Progress bar
	progress_bar = sl.progress(0)

	books_pd = pd.DataFrame(columns = ['Title','Author','Library', 'Location','Call_Number','Availability'])

	for index,book in book_list_pd.iterrows():
		try:
			book_title,book_author,book_copy_pd = GetBookCopyInfo(book['URL'])
			sl.write(book_title)

			# Concatenates dataframe
			books_pd = books_pd.append(book_copy_pd, ignore_index=True)
			book_copy_pd
		except:
			sl.write('Query error:',book_title)

		# Updates progress bar
		total_length = float(len(book_list_pd['URL'].values))
		percent_complete = int(100*float(index+1)/total_length)
		progress_bar.progress(percent_complete)



	books_pd
	if is_save_csv:
		books_pd.to_csv('bookinfo.csv', index=False)
		sl.write('Saved to .csv')