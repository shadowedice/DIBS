from discord.ext import commands
import aiohttp
import asyncio

TWITCH_LIMIT = 25

class Twitch:
    def __init__(self, bot, database, apiID):
        self.bot = bot
        self.database = database
        self.apiID = apiID
        self.session = None
        self.onlineUsers = []
        
        

    async def checkTwitch(self):
        self.session = aiohttp.ClientSession(headers={'Client-ID' : self.apiID})
        while True:
            #For each twitch user check their status
            req = 0
            for user in self.database.GetFields("Users", ["Twitch"], "notNull", ["ServerId", "UserID", "Twitch"]):
                async with self.session.get('https://api.twitch.tv/helix/streams?user_login=' + user[2]) as resp:
                    req += 1
                    json = await resp.json()
                    if json['data']:
                        if user not in self.onlineUsers:
                            self.onlineUsers.append(user)
                            channel = self.database.GetField("BotChannels", ["ServerId", "Type"], [user[0], "Twitch"], ["ChannelID"])
                            if channel:
                                server = self.bot.get_server(user[0])
                                await self.bot.send_message(server.get_channel(channel[0]), "{} went live on Twitch! You can watch their stream here:\n https://www.twitch.tv/{}".format(server.get_member(user[1]).name, user[2]))
                    else:
                        if user in self.onlineUsers:
                            channel = self.database.GetField("BotChannels", ["ServerId", "Type"], [user[0], "Twitch"], ["ChannelID"])
                            if channel:
                                server = self.bot.get_server(user[0])
                                await self.bot.send_message(server.get_channel(channel[0]), "{} has ended their stream.".format(server.get_member(user[1]).name))
                            self.onlineUsers.remove(user)
                if req > TWITCH_LIMIT:
                    await asynico.sleep(60)
                    req = 0
            await asyncio.sleep(30)
            
    @commands.command(pass_context=True)
    async def addTwitch(self, ctx, name : str):
        if self.session:
            async with self.session.get('https://api.twitch.tv/helix/users?login=' + name) as resp:
                json = await resp.json()
                if json['data']:
                    self.database.SetFields("Users", ["ServerID", "UserID"], [ctx.message.server.id, ctx.message.author.id], ["Twitch"], [name])
                    await self.bot.say("I set your twitch name to:  " + name )
                else:
                    await self.bot.say("I'm sorry but I cant find the username: " + name )
        else:
            await self.bot.say("I'm still setting up")
        
    @commands.command(pass_context=True)
    async def removeTwitch(self, ctx):
        self.database.SetFields("Users", ["ServerID", "UserID"], [ctx.message.server.id, ctx.message.author.id], ["Twitch"], [""])
        await self.bot.say("I removed your twitch username.")
        
    async def closeSession(self):
        self.session.close()
        self.session = None