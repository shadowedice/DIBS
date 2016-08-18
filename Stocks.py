from discord.ext import commands
import urllib.request as ur
from bs4 import BeautifulSoup
import os


class Stocks:
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def stock(self, name : str):
        """Grabs the stock graph of your choice"""
        #Insurance against typical Greg shenanigans
        if name.lower() == 'greg':
            await self.bot.say('Greg is currently valued at $0.00. How sad.')
            return
    
        url = 'https://finance.yahoo.com/quote/%s?p=%s' % (name, name)
        stock = ur.urlopen(url).read()
        soup = BeautifulSoup(stock, 'html.parser')
        nameData = " "
        priceData = " "

        h1 = soup.find('h1', class_="D(ib) Fz(18px)")
        if h1 is not None:
            nameData = h1.get_text()
        else:
            await self.bot.say('There is no market data for that ticker value.')
            return
            
        span = soup.find('span', class_="Fw(b) D(ib) Fz(36px) Mb(-4px)")
        if span is not None:
            priceData = span.get_text()
        else:
            await self.bot.say('There is no price data for that ticker value.')
            return

        # If the stock results are not found, Yahoo! redirects to a search
        #if "Search Results" in nameData:
        #    await self.bot.say('There is no market data for that ticker value.')
            
        #Return a string with desired data
        await self.bot.say('Grabbing the stock data for: {}! May the market be ever in your favor!\n\n{}:\nCurrently valued at: ${}'.format(name.upper(), nameData, priceData))
        
        # imageData = soup.find('div', class_="chart")
        # if imageData is None:
        #     await self.bot.say('There is no graph data for that ticker value.')
        # else:
        #     chartURL = imageData.find('img')['src']
        #     imgname = "chart.jpg"
        #     ur.urlretrieve(chartURL, imgname)
        #     await self.bot.upload(imgname)
        #     os.remove(imgname)