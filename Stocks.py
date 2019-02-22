from discord.ext import commands
import aiohttp
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
        else:
            async with aiohttp.request('GET', 'https://api.iextrading.com/1.0/stock/' + name + '/quote') as resp:
                try:
                    tickerInfo = json.loads(await resp.text())
                    change = str(tickerInfo['changePercent'] * 100)
                    #add plus sign for positive value
                    if tickerInfo['changePercent'] > 0:
                        change = "+" + change
                        
                    await self.bot.say("{} ({})\nLast Updated: {}\nValue: ${}\nChange: {}%".format(tickerInfo['companyName'], name.upper(), tickerInfo['latestTime'], tickerInfo['latestPrice'], change))
                except:
                    await self.bot.say("I'm sorry but I can't find {} ticker!".format(name.upper()))
