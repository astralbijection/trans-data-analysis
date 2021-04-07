from collections import namedtuple
from pathlib import Path

import bs4
import pytest

from scrape.ontheissues.candidate import scrape_vote_match

TEST_DIR = Path("resources/test/ontheissues/")

TestCase = namedtuple('TestCase', 'name html stances ballotpedia')

candidates = [
    TestCase(
        name='Stacey Abrams',
        html=(TEST_DIR / "Stacey_Abrams.htm").read_text(encoding='ISO-8859-1'),
        stances=[4, 3, 4, 0, 4, 4, 1, 1, 1, 0, 4, 4, 4, 0, 3, 4, 0, 4, 2, 4],
        ballotpedia='https://ballotpedia.org/Stacey_Abrams'
    ),
    TestCase(
        name='Mike Pence',
        html=(TEST_DIR / "Mike_Pence.htm").read_text(encoding='ISO-8859-1'),
        stances=[0, 0, 1, 4, 0, 3, 4, 3, 3, 4, 0, 0, 4, 4, 4, 1, 1, 0, 4, 1],
        ballotpedia='https://ballotpedia.org/Mike_Pence'
    ),
]


@pytest.mark.parametrize('candidate', candidates)
def test_scrapes_vote_match_from_candidate_page(candidate: TestCase):
    soup = bs4.BeautifulSoup(candidate.html, "html")

    result = scrape_vote_match(soup)

    assert result == candidate.stances
