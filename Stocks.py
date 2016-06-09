from discord.ext import commands
import urllib.request as ur
from bs4 import BeautifulSoup


class Stocks:
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def stock(self, name : str):
        """Grabs the stock graph of your choice"""
        #Insurance against typical Greg shenanigans
        if name.lower() == 'greg':
            return 'Greg is currently valued at $0.00. How sad.'
    
        url = 'http://finance.yahoo.com/q?s={}'.format(name)
        stock = ur.urlopen(url).read()
        soup = BeautifulSoup(stock, 'html.parser')
        nameData = soup.find('div', class_="title")
        if nameData is None:
            await self.bot.say('There is no market data for that ticker value.')
        else:
            companyName = nameData.find('h2').getText()
            priceData = soup.find('span', class_="time_rtq_ticker")
            currentPrice = priceData.getText()
        
            #Return a string with desired data
            await self.bot.say('Grabbing the stock data for: {}! May the market be ever in your favor!\n{}:\nCurrently valued at: ${}'.format(name.upper(), companyName, currentPrice))