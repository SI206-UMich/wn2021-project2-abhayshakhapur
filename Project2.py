from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """
    base_path = os.path.abspath(os.path.dirname(__file__))
    full_path = os.path.join(base_path, filename)
    obj = open(full_path, 'r')
    obj_content = obj.read()
    obj.close()
    soup = BeautifulSoup(obj_content, 'html.parser')
    book_titles = []
    for x in range(20):
        book_tags = soup.find_all('tr', {"itemtype":"http://schema.org/Book"})[x]
        title_tag = book_tags.find('a')
        author_tag = book_tags.find('a', {"class":"authorName"})
        author = author_tag.text
        title = title_tag['title']
        book_titles.append((title.strip(), author.strip()))
    return book_titles
#get_titles_from_search_results('search_results.htm')

def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """
    url = "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc"
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    book_urls = []
    base_url = "goodreads.com"
    for x in range(10):
        book_tags = soup.find_all('tr', {'itemtype':'http://schema.org/Book'})[x]
        url_tag = book_tags.find('a')
        url1 = url_tag['href']
        book_url = base_url+url1
        book_urls.append(book_url.strip())
    return book_urls

def get_book_summary(book_url): 
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """
    request = requests.get(book_url)
    soup = BeautifulSoup(request.text, 'html.parser')
    book_title1 = soup.find('meta', {'property':'og:title'})
    book_title2 = book_title1['content'].strip()
    book_pages1 = soup.find('meta', {'property':'books:page_count'})
    book_pages2 = book_pages1['content'].strip()
    author = " "
    book_author1 = soup.find('title').text
    book_author2 = book_author1.split()
    book_author3 = book_author2[-2:]
    book_author4 = author.join(book_author3)
    book_author5 = book_author4.strip()
    summary = (book_title2, book_author5, book_pages2)
    print(summary)
    return summary

#get_book_summary('https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1')

def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    
    obj = open(filepath, 'r')
    obj_content = obj.read()
    obj.close()
    soup = BeautifulSoup(obj_content, 'html.parser')
    book_summary = []
    for x in range(20):
        best_books_data = soup.find_all('div', {'class':'category clearFix'})[x]
        category1 = best_books_data.find('a').text
        category2 = category1.strip()
        title = best_books_data.find('img')['alt'].strip()
        url = best_books_data.find('a')['href'].strip()
        book_summary.append((category2, title, url))
    #print(book_summary)
    return book_summary
        #print(category2)

#summarize_best_books('best_books_2020.htm')

def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    header = ['Book title', 'Author Name']

    with open(filename, 'w') as File:
        writer = csv.writer(File)
        writer.writerow(header)
        for x in data:
            writer.writerow(x)

#write_csv(get_titles_from_search_results('search_results.htm'), 'search_results.csv')


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    
    obj = open(filepath, 'r')
    obj_content = obj.read()
    obj.close()
    soup = BeautifulSoup(obj_content, 'html.parser')
    book_desc = soup.find('div', {'id':'descriptionContainer'})
    description_text = book_desc.find_all('span')[1].text
    proper_nouns = re.findall(r"(?<!\.\s)(?!^)\b([A-Z][a-z]\w*(?:\s+[A-Z][a-z]\w*)*)", description_text)
    named_entities = []
    named_entities1 = []
    for x in proper_nouns:
        if len(x.split())>1:
            named_entities.append(x)
    for x in named_entities:
        named_entities.append(x.strip())
    print(named_entities1)
    return named_entities1
extra_credit('extra_credit.htm')

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls
    search_urls = get_search_links()

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        results = get_titles_from_search_results('search_results.htm')

        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(results), 20)

        # check that the variable you saved after calling the function is a list
        self.assertEqual(isinstance(results, list), True)

        # check that each item in the list is a tuple
        self.assertEqual(all(isinstance(x, tuple) for x in results), True)

        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(results[0], ('Harry Potter and the Deathly Hallows','J.K. Rowling'))

        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(results[-1], ('Harry Potter: The Prequel (Harry Potter, #0.5)','J.K. Rowling'))

    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        self.assertEqual(isinstance(TestCases.search_urls), True)
        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(TestCases.search_urls), 10)
        # check that each URL in the TestCases.search_urls is a string
        self.assertEqual(all(isinstance(x, str) for x in search_urls), True)
        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        self.assertEqual(all(if 'https://www.goodreads.com/book/show/' in x for x in TestCases.search_urls), True)

    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        # for each URL in TestCases.search_urls (should be a list of tuples)
        summaries = []
        for x in TestCases.search_urls:
            summaries.append(get_book_summary(x))

all(isinstance(n, int) for n in lst)

        # check that the number of book summaries is correct (10)
        self.assertEqual(len(summaries), 10)
            # check that each item in the list is a tuple
        self.assertEqual(all(isinstance(x, tuple) for x in summaries), True)
            # check that each tuple has 3 elements
        self.assertEqual(all(if len(x)==3 for x in summaries), True)
            # check that the first two elements in the tuple are string
        self.assertEqual(isinstance(summaries[1][0], str), True)
        self.assertEqual(isinstance(summaries[1][1], str), True)
            # check that the third element in the tuple, i.e. pages is an int
        self.assertEqual(isinstance(summaries[1][2], int), True)
            # check that the first book in the search has 337 pages
        self.assertEqual(summaries[0][2], 337)

    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        summ = summarize_best_books()
        # check that we have the right number of best books (20)
        self.assertEqual(len(summ), 20)
            # assert each item in the list of best books is a tuple
        self.assertEqual(all(isinstance(x, tuple) for x in summ), True)
            # check that each tuple has a length of 3
        self.assertEqual(all(if len(x)==3 for x in summ), True)
        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(summ[0], ('Fiction', 'The Midnight Library', 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'))
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(summ[-1], ('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'))

    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        var = get_titles_from_search_results(search_results.htm)
        # call write csv on the variable you saved and 'test.csv'
        write_csv(var, 'test.csv')
        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        csv = open('test.csv', 'r')
        lines = csv.readlines()
        csv.close()
        # check that there are 21 lines in the csv
        self.assertEqual(len(lines), 21)
        # check that the header row is correct
        self.assertEqual(lines[0], 'Book title', 'Author Name')
        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        self.assertEqual(lines[1], 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling')
        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        self.assertEqual(lines[-1], 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling')

if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)



