import discord
from discord.ext import commands
from Stocks import Stocks
from MagicCard import MagicCard
from TicTacToe import TicTacToe
from Overwatch import Overwatch
from SoundBoard import SoundBoard
#from SQL_Interaction import SQL_Interaction
from Admin import Admin
import Token

if not discord.opus.is_loaded():
    discord.opus.load_opus("libopus.so")

bot = commands.Bot(command_prefix='$', description='I am here to serve')

soundBoard = SoundBoard(bot)

bot.add_cog(Stocks(bot))
bot.add_cog(MagicCard(bot))
bot.add_cog(TicTacToe(bot))
bot.add_cog(Overwatch(bot))
bot.add_cog(soundBoard)
bot.add_cog(Admin(bot, soundBoard))
#bot.add_cog(SQL_Interaction(bot))


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    
if Token.DiscordToken():
    bot.run(Token.DiscordToken())
else:
    print("No token found. Unable to start DIBS")