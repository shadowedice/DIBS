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
        

    async def checkTwitch(self):
        self.session = aiohttp.ClientSession(headers={'Client-ID' : self.apiID})
        await self.__removeOldMessages()
        while True:
            self.requests = 0
            usrStrReq = ""
            for usr in self.database.GetFields("Users", ["Twitch"], "notNull", ["Twitch"], True):
                usrStrReq += "&user_login=" + usr[0]
            try:
                async with self.session.get('https://api.twitch.tv/helix/streams?' + usrStrReq[1:])  as resp:
                    self.requests += 1
                    if resp.status == 200:
                        json = await resp.json()
                        
                        #check each twitch user (Could be same account on multiple discord servers)
                        for user in self.database.GetFields("Users", ["Twitch"], "notNull", ["ServerId", "UserID", "Twitch"]):
                            channel = self.database.GetField("BotChannels", ["ServerId", "Type"], [user[0], "Twitch"], ["ChannelID"])
                            if channel:
                                msgID = self.database.GetField("TwitchMessages", ["ServerID", "ChannelID", "UserID"], [user[0], channel[0], user[1]], ["MessageID"])
                                server = self.bot.get_server(user[0])
                                #Live user
                                isLive = False;
                                for liveUser in json['data']:
                                    if liveUser['user_name'].lower() == user[2].lower():
                                        isLive = True
                                        gameID = liveUser['game_id']
                                        msgText = "{} is live playing **{}** on Twitch! You can watch their stream here:\nhttps://www.twitch.tv/{}".format(server.get_member(user[1]).name, await self.__getGameName(gameID), user[2])
                                        #if not in the current user list
                                        if not msgID:
                                            message = await self.bot.send_message(server.get_channel(channel[0]), msgText)
                                            self.database.AddEntry("TwitchMessages", ["ServerID", "ChannelID", "MessageID", "UserID"], [user[0], channel[0], message.id, user[1]], [], [])
                                        #Is in list, check for updates
                                        else:
                                            curMsg = await self.bot.get_message(server.get_channel(channel[0]), msgID[0])
                                            if curMsg.content != msgText:
                                                await self.bot.edit_message(curMsg, msgText)
                                #Not live
                                if not isLive:
                                    #Was in live list
                                    if msgID:
                                        await self.bot.delete_message(await self.bot.get_message(server.get_channel(channel[0]), msgID[0]))
                                        self.database.RemoveEntry("TwitchMessages", ["ServerID", "ChannelID", "MessageID"], [user[0], channel[0], msgID[0]])
            except Exception as e:
                print("**Hit exception in checkTwitch()**")
                print(type(e).__name__ + str(e))
                
            await asyncio.sleep(60)
            
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
        gamestr = self.database.GetField("TwitchGameID", ["GameID"], [gameID], ["GameStr"])
        if not gamestr:
            async with self.session.get('https://api.twitch.tv/helix/games?id=' + gameID) as resp:
                self.requests += 1
                if resp.status == 200:
                    json = await resp.json()
                    if json['data']:
                        name = json['data'][0]['name']
                        self.database.AddEntry("TwitchGameID", ["GameID", "GameStr"], [gameID, name], [], [])
                        return name
        else:
            return gamestr[0]
            
    async def __removeOldMessages(self):
        for message in self.database.GetTable("TwitchMessages", ["ServerID", "ChannelID", "MessageID"]):
            try:
                await self.bot.delete_message(await self.bot.get_message(self.bot.get_server(message[0]).get_channel(message[1]), message[2]))
            except  Exception as e:
                print(type(e).__name__ + str(e))   
            self.database.RemoveEntry("TwitchMessages", ["ServerID", "ChannelID", "MessageID"], [message[0], message[1], message[2]])