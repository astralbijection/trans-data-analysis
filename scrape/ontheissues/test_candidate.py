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
        ballotpedia='https://ballotpedia.org/Stacey_Abrams',
    ),
    TestCase(
        name='Mike Pence',
        html=(TEST_DIR / "Mike_Pence.htm").read_text(encoding='ISO-8859-1'),
        stances=[0, 0, 1, 4, 0, 3, 4, 3, 3, 4, 0, 0, 4, 4, 4, 1, 1, 0, 4, 1],
        ballotpedia='https://ballotpedia.org/Mike_Pence',
    ),
    TestCase(
        name='Hillary Clinton',
        html=(TEST_DIR / "Hillary_Clinton.htm").read_text(encoding='ISO-8859-1'),
        stances=[4, 4, 4, 3, 4, 0, 0, 0, 1, 0, 4, 4, 1, 1, 2, 4, 1, 4, 1, 4],
        ballotpedia='https://ballotpedia.org/Hillary_Clinton',
    ),
    TestCase(
        name='Tim Pawlenty',
        html=(TEST_DIR / "Tim_Pawlenty.htm").read_text(encoding='ISO-8859-1'),
        stances=[0, 2, 0, 4, 0, 4, 4, 0, 4, 3, 0, 1, 1, 2, 4, 0, 0, 3, 4, 0],
        ballotpedia='https://ballotpedia.org/Tim_Pawlenty',
    ),
    TestCase(
        name='Mark Sanford',
        html=(TEST_DIR / "Mark_Sanford.htm").read_text(encoding='ISO-8859-1'),
        stances=[0, 4, 1, 3, 1, 3, 4, 3, 3, 2, 0, 1, 3, 2, 3, 4, 2, 1, 2, 0],
        ballotpedia='https://ballotpedia.org/Mark_Sanford',
    ),
]


@pytest.mark.parametrize('candidate', candidates)
def test_scrapes_vote_match(candidate: TestCase):
    soup = bs4.BeautifulSoup(candidate.html, features="lxml")

    result = scrape_vote_match(soup)

    assert result == candidate.stances


@pytest.mark.parametrize('candidate', candidates)
def test_scrapes_name(candidate: TestCase):
    soup = bs4.BeautifulSoup(candidate.html, features="lxml")

    result = get_name(soup)

    assert result == candidate.name


@pytest.mark.parametrize('candidate', candidates)
def test_scrapes_ballotpedia(candidate: TestCase):
    soup = bs4.BeautifulSoup(candidate.html, features="lxml")

    result = get_ballotpedia(soup)

    assert result == candidate.ballotpedia
