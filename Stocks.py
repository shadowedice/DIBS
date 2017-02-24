from discord.ext import commands
from yahoo_finance import Share
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
        stock = Share(name)
        await self.bot.say('Grabbing the stock data for: {}!\n May the market be ever in your favor!\n\n{}:\nCurrently valued at: ${}'.format(name.upper(), stock.get_name(), stock.get_price()))
        