import discord
from discord.ext import commands
from Stocks import Stocks
from MagicCard import MagicCard
from TicTacToe import TicTacToe
from Overwatch import Overwatch
from SoundBoard import SoundBoard
from User import User
from Database import Database
from Holidays import Holidays
import Token

if not discord.opus.is_loaded():
    discord.opus.load_opus("libopus.so")

bot = commands.Bot(command_prefix='$', description='I am here to serve')

database = Database()
soundBoard = SoundBoard(bot,database)
user = User(bot, database, soundBoard)
holidays = Holidays(bot, database)

bot.add_cog(Stocks(bot))
bot.add_cog(MagicCard(bot))
bot.add_cog(TicTacToe(bot))
bot.add_cog(Overwatch(bot))
bot.add_cog(soundBoard)
bot.add_cog(user)
bot.add_cog(holidays)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    for server in bot.servers:
        for member in server.members:
            if not database.FieldExists("Users", ["ServerID", "UserID"], [server.id, member.id]):
                if server.owner.id == member.id:
                    admin = "True"
                else:
                    admin = "False"
                database.AddEntry("Users", ["ServerID", "UserID"], [server.id, member.id], ["Admin", "Mute", "Iam"], [admin, "False", ""])
    
if Token.DiscordToken():
    bot.run(Token.DiscordToken())
else:
    print("No token found. Unable to start DIBS")