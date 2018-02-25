from discord.ext import commands
import urllib.request as ur
import json


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
        data = json.loads(ur.urlopen('http://finance.google.com/finance?q=' + name + '&output=json').read().decode('utf-8')[3:-1])
        await self.bot.say('Grabbing the stock data for: {}!\nMay the market be ever in your favor!\n\n{}:\nCurrently valued at: ${}'.format(data[0]['symbol'], data[0]['name'], data[0]['l']))