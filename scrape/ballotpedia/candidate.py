import re
from urllib.parse import urlparse

import bs4


def get_infobox(soup: bs4.BeautifulSoup):
    return soup.select_one('.infobox.person')


def scrape_contact(tag: bs4.Tag):
    a = tag.find('a')
    text = a.get_text(strip=True)
    href = a.attrs.get('href')

    return text, href


def get_handle_from_href(href: str):
    url = urlparse(href)
    assert url.hostname in ('twitter.com', 'www.twitter.com'), 'Non-twitter URL'
    handle = url.path.replace('/', '')
    return handle


def get_infobox_twitters(soup: bs4.BeautifulSoup):
    infobox = get_infobox(soup)

    contact: bs4.Tag = infobox.find('div', text='Contact')
    assert contact is not None, 'No contacts found in infobox'
    print(contact)
    contacts = [scrape_contact(tag) for tag in contact.find_next_siblings()]
    twitters = [
        (name, get_handle_from_href(href))
        for name, href in contacts
        if 'twitter' in name.lower()
    ]

    return twitters


def get_external_links_twitters(soup: bs4.BeautifulSoup):
    regex = re.compile(r'twitter', flags=re.IGNORECASE)
    twitters = []
    for a in soup.find_all('a', text=regex):
        a: bs4.Tag
        href = a.attrs.get('href')
        name = a.get_text(strip=True)
        if href is None:
            continue

        try:
            handle = get_handle_from_href(href)
        except AssertionError:
            continue

        twitters.append((name, handle))

    return twitters


def get_twitters(soup: bs4.BeautifulSoup):
    try:
        return get_infobox_twitters(soup)
    except AssertionError:
        pass

    return get_external_links_twitters(soup)


def get_party(soup: bs4.BeautifulSoup):
    infobox = get_infobox(soup)
    text = infobox.get_text()
    return re.search(r'(.+) Party', text).group(1).strip()
