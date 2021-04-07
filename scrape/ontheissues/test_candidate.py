from collections import namedtuple
from pathlib import Path

import bs4
import pytest

from scrape.ontheissues.candidate import scrape_vote_match, get_name, get_ballotpedia

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
    TestCase(
        name='Hillary Clinton',
        html=(TEST_DIR / "Hillary_Clinton.htm").read_text(encoding='ISO-8859-1'),
        stances=[4, 4, 4, 3, 4, 0, 0, 0, 1, 0, 4, 4, 1, 1, 2, 4, 1, 4, 1, 4],
        ballotpedia='https://ballotpedia.org/Hillary_Clinton'
    ),
]


@pytest.mark.parametrize('candidate', candidates)
def test_scrapes_vote_match(candidate: TestCase):
    soup = bs4.BeautifulSoup(candidate.html, "html")

    result = scrape_vote_match(soup)

    assert result == candidate.stances


@pytest.mark.parametrize('candidate', candidates)
def test_scrapes_name(candidate: TestCase):
    soup = bs4.BeautifulSoup(candidate.html, "html")

    result = get_name(soup)

    assert result == candidate.name


@pytest.mark.parametrize('candidate', candidates)
def test_scrapes_ballotpedia(candidate: TestCase):
    soup = bs4.BeautifulSoup(candidate.html, "html")

    result = get_ballotpedia(soup)

    assert result == candidate.ballotpedia
