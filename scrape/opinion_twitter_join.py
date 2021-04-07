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


async def fetch_politician(client: ClientSession, ontheissues_uri: str):
    async with client.get(ontheissues_uri) as response:
        html = await response.text()
        print(f'Fetched OTI {ontheissues_uri}')

    soup = bs4.BeautifulSoup(html, features='lxml')
    ballotpedia = get_ballotpedia(soup)
    assert ballotpedia is not None, 'No ballotpedia'

    vote_match = scrape_vote_match(soup)
    name = get_name(soup)
    print(f'Name: {name}; Ballotpedia: {ballotpedia}; Stances: {vote_match}')

    async with client.get(ballotpedia) as response:
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

    print('Got result %s', result)

    return result


async def fetch_politicians(ontheissues_uris: Iterable[str]):
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
    await fetch_single()
    with open('urls.txt', 'r') as files:
        urls = {url.strip() for url in files.readlines()}

    print(f'Fetching {len(urls)} urls')
    responses = await fetch_politicians(urls)

    with open('data.json', 'wb') as file:
        data = [
            dict(r) if isinstance(r, Politician) else repr(r)
            for r in responses
        ]
        json.dump(data, file)


async def fetch_single():
    async with ClientSession() as client:
        print(await fetch_politician(client, 'https://www.ontheissues.org/Mark_Sanford.htm'))


if __name__ == '__main__':
    asyncio.run(main())
