from discord.ext import commands
import urllib.request as ur
import json


class Stocks:
    def __init__(self, bot, token):
        self.bot = bot
        self.token = token
        
    #Currently uses Alphavantage API. You will need your own API key in order to run
    @commands.command()
    async def stock(self, name : str):
        """Grabs the stock graph of your choice"""
        #Insurance against typical Greg shenanigans
        if name.lower() == 'greg':
            await self.bot.say('Greg is currently valued at $0.00. How sad.')
            return
        if not self.token:
            await self.bot.say("I'm sorry but no API key for Alphavantage has been provided. Unable to retrieve stock data")
        else:
            data = json.loads(ur.urlopen('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + name + '&apikey=' + self.token).read().decode('utf-8'))
            if 'Error Message' in data:
                await self.bot.say("I'm sorry but I can't find {} ticker!".format(name.upper()))
                return
            date = data['Meta Data']['3. Last Refreshed']
            value = data['Time Series (Daily)'][date]['4. close']
            await self.bot.say('Grabbing the stock data for: {}!\nMay the market be ever in your favor!\n\nCurrently valued at: ${}'.format(name.upper(), value))