from urllib.parse import urlparse

import bs4


def get_infobox(soup: bs4.BeautifulSoup):
    return soup.select_one('.infobox.person')


def scrape_contact(tag: bs4.Tag):
    a = tag.find('a')
    text = a.get_text(strip=True)
    href = a.attrs.get('href')

    return text, href


def get_handle_from_url(href):
    url = urlparse(href)
    assert url.hostname in ('twitter.com', 'www.twitter.com'), 'Non-twitter URL'
    handle = url.path.replace('/', '')
    return handle


def get_twitters(soup: bs4.BeautifulSoup):
    infobox = get_infobox(soup)

    contact: bs4.Tag = infobox.find('div', text='Contact')
    contacts = [scrape_contact(tag) for tag in contact.find_next_siblings()]
    twitters = [
        (name, get_handle_from_url(href))
        for name, href in contacts
        if 'twitter' in name.lower()
    ]

    return twitters
