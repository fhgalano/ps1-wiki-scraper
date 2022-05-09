import requests
from bs4 import BeautifulSoup
import re

url_cache = dict()
all_emails = dict()


def rec_scraper(url, max_depth=2):
    # get html info
    page = requests.get(url)

    # check status
    if page.status_code != 200:
        url_cache[url] = None
        print(max_depth, url)
        return

    # make the soup
    data = BeautifulSoup(page.text, features="html.parser")

    # search for links to other wiki pages
    possible_links = data.find_all('a')
    links = [link for link in possible_links if 'href' in str(link)]

    wiki_links = []
    for link in possible_links:
        if link.get('href'):
            is_wiki_link = 'wiki.pumpingstationone' in link['href']
            is_wiki_extension = link['href'][0] == '/'
            if is_wiki_extension:
                wiki_links.append('https://wiki.pumpingstationone.org' + link['href'])
            elif is_wiki_link:
                wiki_links.append(link['href'])

    # search for emails
    emails = []
    search = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', data.text)
    if search:
        [emails.append(email) for email in search]

    # cache url and the emails
    if not url_cache.get(url):
        url_cache[url] = emails
        if emails:
            all_emails[url] = emails

    # recursively search if not at depth
    if max_depth > 0:
        max_depth -= 1
        for link in wiki_links:
            if link not in url_cache:
                rec_scraper(link, max_depth=max_depth)

    # print(emails)
    return emails


if __name__ == '__main__':
    # get starting page (ps1 main page)
    starting_page = 'https://wiki.pumpingstationone.org/'
    # starting_page = 'https://wiki.pumpingstationone.org/Category:Wood_Shop'

    rec_scraper(starting_page, max_depth=2)
    for emails in all_emails.items():
        for email in emails:
            print(email)
