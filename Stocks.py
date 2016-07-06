from discord.ext import commands
import urllib.request as ur
from bs4 import BeautifulSoup
import os


class Stocks:
    def __init__(self, bot):
        self.bot = bot
    
    def card_image(self):
        link = "http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=%s&type=card" % self.cardId
        imgname = self.cardId + ".jpg"
        ur.urlretrieve(link, imgname)
        return imgname
        
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
        
        imageData = soup.find('div', class_="chart")
        if imageData is None:
            await self.bot.say('There is no graph data for that ticker value.')
        else:
            chartURL = imageData.find('img')['src']
            imgname = "chart.jpg"
            ur.urlretrieve(chartURL, imgname)
            await self.bot.upload(imgname)
            os.remove(imgname)