from discord.ext import commands
import urllib.request as ur
from bs4 import BeautifulSoup, Tag

class Overwatch:
    def __init__(self,bot):
        self.bot = bot
        self.playerId = ''
        
    @commands.command()
    async def overwatch(self, username : str, query : str):
        self.playerId = username.replace('#', '-')
        link = "https://playoverwatch.com/en-us/career/pc/us/%s" % self.playerId
        page = ur.urlopen(link).read()
        
        soup = BeautifulSoup(page, 'html.parser')
        
        ret = "These are the stats for " + self.playerId
        
        if query == "quick":
            quickStats = soup.find('div', attrs={'id':'quick-play'}).find('div', attrs={'data-category-id':'0x02E00000FFFFFFFF'})
            for statTitle in quickStats.find_all('table'):
                ret += "\n**" + statTitle.find('span', class_="stat-title").get_text() + "**\n-----------------------------------------" + "\n"
                body = statTitle.find('tbody')
                for stat in body.find_all('tr'):
                    ret += stat.find('td').get_text() + ": " + stat.find('td').findNext('td').get_text() + "\n"
        elif query == "competitive":
            compStats = soup.find('div', attrs={'id':'competitive-play'}).find('div', attrs={'data-category-id':'0x02E00000FFFFFFFF'})
            for statTitle in compStats.find_all('table'):
                ret += "\n**" + statTitle.find('span', class_="stat-title").get_text() + "**\n-----------------------------------------" + "\n"
                body = statTitle.find('tbody')
                for stat in body.find_all('tr'):
                    ret += stat.find('td').get_text() + ": " + stat.find('td').findNext('td').get_text() + "\n"
        elif query == "quickFeat":
            for card in soup.find('div', attrs={'id':'quick-play'}).find_all('div', class_="card-content"):
                ret += card.find('p', class_="card-copy").get_text() + ": "
                ret += card.find('h3', class_="card-heading").get_text() + "\n"
        elif query == "compFeat":
            for card in soup.find('div', attrs={'id':'competitive-play'}).find_all('div', class_="card-content"):
                ret += card.find('p', class_="card-copy").get_text() + ": "
                ret += card.find('h3', class_="card-heading").get_text() + "\n"
        
        await self.bot.say(ret)
        
        