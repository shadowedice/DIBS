from discord.ext import commands
import aiohttp
import json


class Stocks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    # Currently uses iextrading
    @commands.command()
    async def stock(self, ctx, name: str):
        """Grabs the stock graph of your choice"""
        # Insurance against typical Greg shenanigans
        if name.lower() == 'greg':
            await ctx.send('Greg is currently valued at $0.00. How sad.')
        else:
            async with aiohttp.request('GET', 'https://api.iextrading.com/1.0/stock/' + name + '/quote') as resp:
                try:
                    tickerInfo = json.loads(await resp.text())
                    change = str(round(tickerInfo['changePercent'] * 100.0, 2))
                    # add plus sign for positive value
                    if tickerInfo['changePercent'] > 0:
                        change = "+" + change
                        
                    await ctx.send("{} ({})\nLast Updated: {}\nValue: ${}\nChange: {}%".format(tickerInfo['companyName'], name.upper(), tickerInfo['latestTime'], tickerInfo['latestPrice'], change))
                except Exception as e:
                    print(type(e).__name__ + str(e))
                    await ctx.send("I'm sorry but I can't find {} ticker!".format(name.upper()))
