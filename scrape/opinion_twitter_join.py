import asyncio
import json
from collections import namedtuple
from typing import Iterable

import bs4
from aiohttp import ClientSession
from asyncio_throttle import Throttler

from scrape.ballotpedia.candidate import get_twitters, get_party
from scrape.ontheissues.candidate import scrape_vote_match, get_name, get_ballotpedia

Politician = namedtuple(
    'Politician',
    'name vote_match ontheissues ballotpedia party twitters'
)

oti_throttler = Throttler(rate_limit=30, period=1)
ballotpedia_throttler = Throttler(rate_limit=30, period=1)


async def fetch_politician(client: ClientSession, ontheissues_uri: str):
    async with oti_throttler, client.get(ontheissues_uri) as response:
        html = await response.text()
        print(f'Fetched OTI {ontheissues_uri}')

    soup = bs4.BeautifulSoup(html, features='lxml')
    name = get_name(soup)
    vote_match = scrape_vote_match(soup)
    ballotpedia = get_ballotpedia(soup)
    if ballotpedia is None:
        return Politician(
            name=name,
            vote_match=vote_match,
            ontheissues=ontheissues_uri,
            ballotpedia=ballotpedia,
            party=None,
            twitters=[],
        )

    print(f'Name: {name}; Ballotpedia: {ballotpedia}; Stances: {vote_match}')

    async with ballotpedia_throttler, client.get(ballotpedia) as response:
        html = await response.text()
        print(f'Fetched Ballotpedia {ontheissues_uri}')

    soup = bs4.BeautifulSoup(html, features="lxml")
    party = get_party(soup)
    twitters = get_twitters(soup)

    result = Politician(
        name=name,
        vote_match=vote_match,
        ontheissues=ontheissues_uri,
        ballotpedia=ballotpedia,
        party=party,
        twitters=twitters,
    )

    print('Got result', result)

    return result


async def fetch_politicians(ontheissues_uris: Iterable[str]):
    async with ClientSession() as client:
        tasks = [
            fetch_politician(client, uri)
            for uri in ontheissues_uris
        ]

        return await asyncio.gather(*tasks, return_exceptions=True)


async def main():
    with open('urls.txt', 'r') as files:
        urls = {url.strip() for url in files.readlines()}

    print(f'Fetching {len(urls)} urls')
    responses = await fetch_politicians(urls)

    with open('politicians.json', 'w') as file:
        # noinspection PyProtectedMember
        data = [
            r._asdict()
            for r in responses
            if isinstance(r, Politician)
        ]
        json.dump(data, file, indent=2)


async def fetch_single():
    async with ClientSession() as client:
        print(await fetch_politician(client, 'https://www.ontheissues.org/TX/Ralph_Moody_Hall.htm'))


if __name__ == '__main__':
    asyncio.run(main())
