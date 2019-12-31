import requests
from bs4 import BeautifulSoup

base_url = "https://www.cricbuzz.com"


def get_cricbuzz_tournaments():
    archive_url = base_url + "/cricket-scorecard-archives"
    req = requests.get(archive_url)

    soup = BeautifulSoup(req.content, "html5lib")
    rows = soup.findAll('a', attrs={'class': 'cb-sch-tms-widgt cb-font-12 cb-arch-yr-tabs'})

    tournaments = []
    for row in rows:
        link = row['href']
        year_url = base_url + link
        r = requests.get(year_url)
        list_soup = BeautifulSoup(r.content, "html5lib")
        year_series = list_soup.findAll(lambda tag: tag.name == 'a' and tag.get('class') == ['text-hvr-underline'])
        for series in year_series:
            tournament = {'name': series['title'], 'url': base_url + series['href']}
            tournaments.append(tournament.copy())

    return tournaments


def get_tournament_games(url):
    r = requests.get(url)
    games_soup = BeautifulSoup(r.content, "html5lib")
    games_links = games_soup.findAll(lambda tag: tag.name == 'a' and tag.get('class') == ['text-hvr-underline'])
    games = []
    for link in games_links:
        game = {'game': link.text, 'url': base_url + link['href']}
        games.append(game.copy())

    return games


def get_cricbuzz_data():
    tournaments = get_cricbuzz_tournaments()

    for tournament in tournaments:
        tournament_url = tournament['url']
        games = get_tournament_games(tournament_url)


url = 'https://www.cricbuzz.com/scores-home/2922/sri-lanka-tour-of-pakistan-test-series-2019'
games = get_tournament_games(url)
print(games)