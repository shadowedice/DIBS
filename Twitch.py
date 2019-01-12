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
        self.requests = 0
        self.onlineUsers = []
        self.gamesDict = {}
        
        

    async def checkTwitch(self):
        self.session = aiohttp.ClientSession(headers={'Client-ID' : self.apiID})
        while True:
            #For each twitch user check their status
            self.requests = 0
            for user in self.database.GetFields("Users", ["Twitch"], "notNull", ["ServerId", "UserID", "Twitch"]):
                channel = self.database.GetField("BotChannels", ["ServerId", "Type"], [user[0], "Twitch"], ["ChannelID"])
                if channel:
                    async with self.session.get('https://api.twitch.tv/helix/streams?user_login=' + user[2]) as resp:
                        self.requests += 1
                        json = await resp.json()
                        curUser = [x for x in self.onlineUsers if x[0] == user[0] and x[1] == user[1] and x[2] == user[2]]
                        server = self.bot.get_server(user[0])
                        #If live
                        try:
                            if json['data']:
                                gameID = json['data'][0]['game_id']
                                msgText = "{} is live playing **{}** on Twitch! You can watch their stream here:\n https://www.twitch.tv/{}".format(server.get_member(user[1]).name, await self.__getGameName(gameID), user[2])
                                #if not in the current user list
                                if not curUser:
                                    message = await self.bot.send_message(server.get_channel(channel[0]), msgText)
                                    self.onlineUsers.append(user + (message.id,))
                                #Is in list, check for updates
                                else:
                                    curMsg = await self.bot.get_message(server.get_channel(channel[0]), curUser[0][3])
                                    if curMsg.content != msgText:
                                        await self.bot.edit_message(curMsg, msgText)
                            #Not live
                            else:
                                #Was in live list
                                if curUser:
                                    await self.bot.delete_message(await self.bot.get_message(server.get_channel(channel[0]), curUser[0][3]))
                                    self.onlineUsers.remove(curUser[0])
                        except KeyError:
                            print("Data not found in response")
                            print(json)
                                
                if self.requests > TWITCH_LIMIT:
                    await asynico.sleep(60)
                    self.requests = 0
            await asyncio.sleep(10)
            
    @commands.command(pass_context=True)
    async def addTwitch(self, ctx, name : str):
        if self.session:
            async with self.session.get('https://api.twitch.tv/helix/users?login=' + name) as resp:
                json = await resp.json()
                try:
                    if json['data']:
                        self.database.SetFields("Users", ["ServerID", "UserID"], [ctx.message.server.id, ctx.message.author.id], ["Twitch"], [name])
                        await self.bot.say("I set your twitch name to:  " + name )
                    else:
                        await self.bot.say("I'm sorry but I cant find the username: " + name )
                    
                except KeyError:
                    print("Data not found in response")
                    print(json)
        else:
            await self.bot.say("I'm still setting up")
        
    @commands.command(pass_context=True)
    async def removeTwitch(self, ctx):
        self.database.SetFields("Users", ["ServerID", "UserID"], [ctx.message.server.id, ctx.message.author.id], ["Twitch"], [""])
        await self.bot.say("I removed your twitch username.")
        
    async def closeSession(self):
        self.session.close()
        self.session = None
        
    async def __getGameName(self, gameID):
        if gameID not in self.gamesDict:
            async with self.session.get('https://api.twitch.tv/helix/games?id=' + gameID) as resp:
                self.requests += 1
                json = await resp.json()
                try:
                    if json['data']:
                        name = json['data'][0]['name']
                        self.gamesDict[gameID] = name
                        return name
                        
                except KeyError:
                    print("Data not found in response")
                    print(json)
                    return name
        else:
            return self.gamesDict[gameID]