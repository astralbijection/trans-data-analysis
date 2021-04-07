import re
from typing import List

import bs4

NORMALIZE_STANCE = {
    'Strongly Favors': 4,
    'Favors': 3,
    'No opinion on': 2,
    'Opposes': 1,
    'Strongly Opposes': 0,
}


def scrape_vote_match_row(row: bs4.Tag):
    first_cell: bs4.Tag = row.findChildren('td')[0]
    stance = first_cell.find('b').get_text(strip=True)
    normalized_stance = NORMALIZE_STANCE[stance]

    # noinspection PyArgumentList
    topic_n_text = first_cell.get_text(separator=' ', strip=True)
    match = re.search(r'topic (\d{1,2}):', topic_n_text)
    topic_n = int(match.group(1))

    return topic_n, normalized_stance


def scrape_vote_match(soup: bs4.BeautifulSoup):
    title: bs4.NavigableString = soup.find(text='VoteMatch Responses')
    table: bs4.Tag = title.find_parent(name='table')
    rows: List[bs4.Tag] = table.findChildren('tr')

    topics = [scrape_vote_match_row(r) for r in rows[2:]]

    assert all(
        topic_n - 1 == i
        for i, (topic_n, stance) in enumerate(topics)
    ), 'Topic numbers do not match up with indices!'

    return [stance for _, stance in topics]
