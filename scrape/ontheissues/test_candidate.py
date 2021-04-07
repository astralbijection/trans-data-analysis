import bs4

from scrape.ontheissues.candidate import scrape_vote_match

stacey_abrams = [4, 3, 4, 0, 4, 4, 1, 1, 1, 0, 4, 4, 4, 0, 3, 4, 0, 4, 2, 4]


def test_scrapes_vote_match_from_candidate_page():
    with open("resources/test/ontheissues/Stacey_Abrams.htm", encoding='ISO-8859-1') as file:
        markup = file.read()
    soup = bs4.BeautifulSoup(markup, "html")

    result = scrape_vote_match(soup)

    assert result == stacey_abrams
