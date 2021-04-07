import asyncio
from collections import namedtuple
from typing import List

import bs4
from aiohttp import ClientSession
from asyncio_throttle import Throttler

from scrape.ballotpedia.candidate import get_twitters, get_party
from scrape.ontheissues.candidate import scrape_vote_match, get_name, get_ballotpedia

Politician = namedtuple(
    'Politician',
    'name vote_match ontheissues ballotpedia party twitters'
)


async def fetch_politician(client: ClientSession, ontheissues_uri: str):
    async with client.get(ontheissues_uri) as response:
        print(f'Fetching {ontheissues_uri}')
        html = await response.text()

    soup = bs4.BeautifulSoup(html, 'html')
    vote_match = scrape_vote_match(soup)
    name = get_name(soup)
    ballotpedia = get_ballotpedia(soup)

    async with client.get(ballotpedia) as response:
        html = await response.text()

    soup = bs4.BeautifulSoup(html, features="lxml")
    party = get_party(soup)
    twitters = get_twitters(soup)

    return Politician(
        name=name,
        vote_match=vote_match,
        ontheissues=ontheissues_uri,
        ballotpedia=ballotpedia,
        party=party,
        twitters=twitters,
    )


async def fetch_politicians(ontheissues_uris: List[str]):
    throttler = Throttler(rate_limit=0.2)

    async with ClientSession() as client:
        async def worker(uri):
            async with throttler:
                return await fetch_politician(client, uri)

        tasks = [
            worker(uri)
            for uri in ontheissues_uris
        ]

        return await asyncio.gather(*tasks, return_exceptions=True)


async def main():
    responses = await fetch_politicians(
        ['https://www.ontheissues.org/Stacey_Abrams.htm',
         'https://www.ontheissues.org/Hillary_Clinton.htm'])
    print('Got responses')
    for i in responses:
        print(repr(i))


if __name__ == '__main__':
    asyncio.run(main())
