from pathlib import Path

import bs4


def get_candidates(soup: bs4.BeautifulSoup):
    political_leaders = soup.find(text='Political Leaders:').find_parent('big')
    tables = political_leaders.find_next_siblings('table')

    links = []
    for table in tables:
        for a in table.select('td a'):
            name = a.text

            href = a.attrs.get('href')
            if href is None:
                continue

            links.append((name, href))

    def find_index_of(keyword):
        filtered = filter(lambda x: keyword in x[1][0], enumerate(links))
        i, _ = next(filtered)
        return i

    trump_i = find_index_of('Trump')
    dnc_i = find_index_of('DNC Platform')
    hw_bush_i = find_index_of('H.W. Bush')
    home_i = find_index_of('Home')

    return links[trump_i:dnc_i] + links[hw_bush_i:home_i]


def get_uris():
    test_dir = Path("resources/test/ontheissues/")
    html = (test_dir / "Candidates.htm").read_text(encoding='ISO-8859-1')
    result = get_candidates(bs4.BeautifulSoup(html, features="lxml"))
    return result


if __name__ == '__main__':
    print(get_uris())
