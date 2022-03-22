import requests
from bs4 import BeautifulSoup
import requests_cache

# Do the same with https://stacker.com/stories/1587/100-best-movies-all-time

requests_cache.install_cache('demo_cache')


class ImdbScraper(object):

    def __init__(self, url):
        self. url = url
        self.description = {}
        self.available_champions_list = {}
        self.upcoming_cost_reductions = {}
        self.scrapped_champion_list = {}
        self.trivia = {}
        self.references = {}
        self.references_table = {}

    def get_request(self):
        return requests.get(self.url).text

    def get_soup(self):
        return BeautifulSoup(self.get_request(), 'html.parser')

    # List of champions

    def get_description(self):
        content = self.get_soup().find('main', class_="page__main")
        title = content.select('h1.page-header__title')[0].get_text().strip()

        text = content.find('div', class_="mw-parser-output")

        link_container = text.find('div', class_="dablink")
        link = link_container.get_text() + ' ' + self.url.replace('/wiki/List_of_champions', '') + link_container.find('a')['href']

        description = text.find('p').get_text().strip()
        
        title2 = content.select('span.mw-headline')[0].get_text().strip()

        self.description = {'title': title, 'link': link, 'description': description, 'title2': title2}

        return self.description

    # List of available champions

    def get_available_champions_list(self):
        content = self.get_soup().find('main', class_="page__main")
        table = content.find('table', class_="article-table")
        rows = table.find_all('tr')

        for row in rows:
            columns = row.find_all(['th', 'td'])
            save = []

            for cell in columns:
                title_info = list(map(lambda data: data.get_text().strip(), cell))
                save.append(list(filter(lambda data: data, title_info)))

            self.available_champions_list[f'{" ".join(save[1])} | {save[2][0]} | {save[3][0]} | {save[4][0]}'] = save[0][0]

        return self.available_champions_list

    # Upcoming cost reductions

    def get_upcoming_cost_reductions(self):
        content = self.get_soup().find('main', class_="page__main")
        title = content.find(attrs={'id':'Upcoming_Cost_Reductions'})

        description = content.find('dd').find('i').get_text().strip().split('history')

        list = title.parent.find_next_sibling('ul').get_text()

        self.upcoming_cost_reductions = {'title': title.get_text().strip(), 'description1': description[0], 'description2': description[1], 'list': list}

        return self.upcoming_cost_reductions

    # List of Scrapped Champions
    def get_scrapped_champion_list(self):
        title = self.get_soup().find(attrs={'id':'List_of_Scrapped_Champions'})

        list = self.get_soup().find('div', class_='columntemplate').find_all('li')

        save = []
        for li in list:
            save.append(li.get_text().strip())

        self.scrapped_champion_list = {'title': title.get_text().strip(), 'list': save}

        return self.scrapped_champion_list

    # Trivia

    def get_trivia(self):
        title = self.get_soup().find(attrs={'id':'Trivia'})

        list = title.parent.find_next_sibling().find_all('li')

        save = []
        for li in list:
            save.append(li.get_text().strip())

        self.trivia = {'title': title.get_text().strip(), 'list': save}

        return self.trivia

    # References

    def get_references(self):
        title = self.get_soup().find(attrs={'id':'References'})

        content = self.get_soup().find('div', class_="navbox-wrapper")

        table_title = content.find('div', class_="mw-collapsible-header").get_text()

        table = content.find('tbody')
        # print(table)

        rows = table.find_all('tr')
        for row in rows:
            columns = row.find_all(['th','td'])
            save = []
            for cell in columns:
                title_info = list(map(lambda data: data.get_text().strip(), cell))
                save.append(list(filter(lambda data: data, title_info)))
            self.references_table[f'{" ".join(save[0])}'] = save[1][0]


        self.references = {'title': title.get_text().strip(), 'table_title': table_title, 'table': self.references_table}

        return self.references

if __name__ == "__main__":

    # List of champions

    description = ImdbScraper(r'https://leagueoflegends.fandom.com/wiki/List_of_champions').get_description()

    print(description['title'].upper() + '\n\n' + description['link'] + '\n' + description['description'] + '\n\n' + description['title2'].upper() + '\n') 

    # List of Available Champions

    available_champions_list = ImdbScraper(r'https://leagueoflegends.fandom.com/wiki/List_of_champions').get_available_champions_list()

    for carac, champion in available_champions_list.items():
        print(f"{champion.upper()} | {carac}")

    # Upcoming Cost Reductions
    upcoming_cost_reductions = ImdbScraper(r'https://leagueoflegends.fandom.com/wiki/List_of_champions').get_upcoming_cost_reductions()

    print('\n' + upcoming_cost_reductions['title'].upper()+ '\n\n' + upcoming_cost_reductions['description1']+ '\n' + upcoming_cost_reductions['description2'] + '\n\n' + upcoming_cost_reductions['list'] + '\n')


    # List of Scrapped Champions
    scrapped_champion_list = ImdbScraper(r'https://leagueoflegends.fandom.com/wiki/List_of_champions').get_scrapped_champion_list()

    print(scrapped_champion_list['title'].upper() + '\n')

    for champion in scrapped_champion_list['list']:
        print('- ' + champion)

    # Trivia

    trivia = ImdbScraper(r'https://leagueoflegends.fandom.com/wiki/List_of_champions').get_trivia()

    print('\n' + trivia['title'].upper() + '\n')

    for champion in trivia['list']:
        print('- ' + champion)

    # References

    references = ImdbScraper(r'https://leagueoflegends.fandom.com/wiki/List_of_champions').get_references()

    print('\n' + references['title'].upper() + '\n\n' + references['table_title'])

    border = ''
    for i in range(len(references['table_title'])):
        border = border + '-'

    print(border)

    for cell in references['table']:
        print(cell)
