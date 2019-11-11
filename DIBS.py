import discord
from discord.ext import commands
from Stocks import Stocks
from MagicCard import MagicCard
from TicTacToe import TicTacToe
from SoundBoard import SoundBoard
from User import User
from Database import Database
from Holidays import Holidays
from Twitch import Twitch
import Token
import asyncio
from contextlib import suppress

if not discord.opus.is_loaded():
    discord.opus.load_opus("libopus.so")

bot = commands.Bot(command_prefix='$', description='I am here to serve')

database = Database()
soundBoard = SoundBoard(bot, database)
user = User(bot, database, soundBoard)
holidays = Holidays(bot, database)
twitch = Twitch(bot, database, Token.TwitchApiId())

bot.add_cog(Stocks(bot))
bot.add_cog(MagicCard(bot))
bot.add_cog(TicTacToe(bot))
bot.add_cog(soundBoard)
bot.add_cog(user)
bot.add_cog(holidays)
bot.add_cog(twitch)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    for guild in bot.guilds:
        for member in guild.members:
            if not database.FieldExists("Users", ["ServerID", "UserID"], [guild.id, member.id]):
                if guild.owner.id == member.id:
                    admin = "True"
                else:
                    admin = "False"
                database.AddEntry("Users", ["ServerID", "UserID"], [guild.id, member.id], ["Admin", "Mute", "Iam"],
                                  [admin, "False", ""])
                
    # add startHoliday to the event loop
    bot.loop.create_task(bot.get_cog("Holidays").startHoliday())
    bot.loop.create_task(bot.get_cog("Twitch").checkTwitch())

    
if Token.DiscordToken():
    try:
        bot.loop.run_until_complete(bot.start(Token.DiscordToken()))
    except Exception as e:
        print("Hit exception in DIBS main")
        print(e)
    finally:
        # get all pending tasks and cancel them
        pending = asyncio.Task.all_tasks()
        for task in pending:
            task.cancel()
            with suppress(asyncio.CancelledError):
                bot.loop.run_until_complete(task)
                
        bot.loop.run_until_complete(twitch.closeSession())
        bot.loop.run_until_complete(bot.logout())
        bot.loop.close()

else:
    print("No token found. Unable to start DIBS")
