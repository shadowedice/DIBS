import discord
from discord.ext import commands
from Stocks import Stocks
from Monaco import Monaco
from MagicCard import MagicCard
from FFXIV import FFXIV
import Token

if not discord.opus.is_loaded():
    discord.opus.load_opus("libopus.so")

bot = commands.Bot(command_prefix='$', description='I am here to serve')

bot.add_cog(Stocks(bot))
bot.add_cog(Monaco(bot))
bot.add_cog(MagicCard(bot))
bot.add_cog(FFXIV(bot))

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
	
bot.run(Token.get_token())