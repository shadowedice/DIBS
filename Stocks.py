from discord.ext import commands
import urllib.request as ur
import json


class Stocks:
    def __init__(self, bot):
        self.bot = bot
        
    #Currently uses iextrading
    @commands.command()
    async def stock(self, name : str):
        """Grabs the stock graph of your choice"""
        #Insurance against typical Greg shenanigans
        if name.lower() == 'greg':
            await self.bot.say('Greg is currently valued at $0.00. How sad.')
            return
        else:
            data = json.loads(ur.urlopen('https://api.iextrading.com/1.0/stock/' + name + '/quote').read().decode('utf-8'))
            if 'Error Message' in data:
                await self.bot.say("I'm sorry but I can't find {} ticker!".format(name.upper()))
                return
            await self.bot.say("{} ({})\nLast Updated: {}\nValue: ${}".format(data['companyName'], name.upper(), data['latestTime'], data['latestPrice']))