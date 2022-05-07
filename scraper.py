import requests
from bs4 import BeautifulSoup
import re


def rec_scraper(url, max_depth=2):
    # get html info
    page = requests.get(url)

    # check status
    if page.status_code != 200:
        exit()

    # make the soup
    data = BeautifulSoup(page.text)

    # search for links to other wiki pages
    possible_links = data.find_all('a')
    links = [link for link in possible_links if 'href' in str(link) and 'wiki.pumping' in str(link)]

    # search for emails
    emails = []
    search = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', data.text)
    if search:
        [emails.append(email) for email in search]

    # recursively search if not at depth
    if max_depth > 0:
        max_depth -= 1
        for link in links:
            rec_scraper(link['href'], max_depth=max_depth)

    print(emails)
    return emails


if __name__ == '__main__':
    # get starting page (ps1 main page)
    # starting_page = 'https://wiki.pumpingstationone.org/'
    starting_page = 'https://wiki.pumpingstationone.org/Category:Wood_Shop'

    rec_scraper(starting_page)
    print('debug')
