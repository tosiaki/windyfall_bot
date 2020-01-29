import random
import requests
from bs4 import BeautifulSoup

def get_random_quote():
    page_number = random.randint(1,101)
    page_query = { 'page': page_number }
    URL = 'https://www.goodreads.com/quotes/tag/inspiration'
    page = requests.get(URL, params=page_query)

    soup = BeautifulSoup(page.content, 'html.parser')
    [s.extract() for s in soup('br')]

    quotes = soup.find_all('div', class_='quoteDetails')
    quote_entry = random.choice(quotes)

    author_or_title = quote_entry.find_all('span', class_='authorOrTitle')
    dash_line = author_or_title[0].previous_sibling
    quotation_lines = dash_line.previous_siblings
    quote = []
    for line in quotation_lines :
        quote.insert(0, line.strip())
    lines = len(quote)
    full_quote = '\n'.join(quote)
    author_line = author_or_title[0].string.strip().rstrip(',')

    likes_text = quote_entry.find_all('a', class_='smallText')
    words_in_likes = likes_text[0].string.split()
    number_of_likes = [int(s) for s in words_in_likes if s.isdigit()]
    likes = number_of_likes[0]    

    return {
            'full_quote': full_quote,
            'author_line': author_line,
            'lines': lines,
            'likes': likes
            }

def get_quote_with_conditions(lines, likes):
    quote = get_random_quote()
    while quote['lines'] > lines or quote['likes'] < likes:
        quote = get_random_quote()
    return quote
