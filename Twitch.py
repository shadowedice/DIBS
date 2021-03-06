from discord.ext import tasks, commands
import aiohttp
from datetime import datetime, timedelta

TWITCH_LIMIT = 25


class Twitch(commands.Cog):
    def __init__(self, bot, database, clientID, clientSecret):
        self.bot = bot
        self.database = database
        self.clientID = clientID
        self.clientSecret = clientSecret
        self.session = None
        self.requests = 0
        self.oathToken = ''
        self.oathExpiration = datetime.now()
        self.headers = {}
        self.checkTwitch.start()

    def cog_unload(self):
        self.checkTwitch.cancel()

    @tasks.loop(seconds=60.0)
    async def checkTwitch(self):
        self.requests = 0
        if self.oathExpiration < (datetime.now() + timedelta(seconds=60)):
            await self.__getOathToken()
        usrStrReq = ""
        for usr in self.database.GetFields("Users", ["Twitch"], "notNull", ["Twitch"], True):
            usrStrReq += "&user_login=" + usr[0]
        try:
            async with self.session.get('https://api.twitch.tv/helix/streams?' + usrStrReq[1:], headers=self.headers) as resp:
                self.requests += 1
                if resp.status == 200:
                    json = await resp.json()

                    # check each twitch user (Could be same account on multiple discord servers)
                    for user in self.database.GetFields("Users", ["Twitch"], "notNull",
                                                        ["ServerId", "UserID", "Twitch"]):
                        channel = self.database.GetField("BotChannels", ["ServerId", "Type"], [user[0], "Twitch"],
                                                         ["ChannelID"])
                        if channel:
                            msgID = self.database.GetField("TwitchMessages", ["ServerID", "ChannelID", "UserID"],
                                                           [user[0], channel[0], user[1]], ["MessageID"])
                            guild = self.bot.get_guild(user[0])
                            # Live user
                            isLive = False
                            for liveUser in json['data']:
                                if liveUser['user_name'].lower() == user[2].lower():
                                    isLive = True
                                    gameID = liveUser['game_id']
                                    msgText = "{} is live playing **{}** on Twitch! You can watch their stream here:\nhttps://www.twitch.tv/{}".format(
                                        guild.get_member(user[1]).name, await self.__getGameName(gameID), user[2])
                                    # if not in the current user list
                                    if not msgID:
                                        message = await guild.get_channel(channel[0]).send(msgText)
                                        self.database.AddEntry("TwitchMessages",
                                                               ["ServerID", "ChannelID", "MessageID", "UserID"],
                                                               [user[0], channel[0], message.id, user[1]], [], [])
                                    # Is in list, check for updates
                                    else:
                                        curMsg = await guild.get_channel(channel[0]).fetch_message(msgID[0])
                                        if curMsg.content != msgText:
                                            await curMsg.edit(content=msgText)
                            # Not live
                            if not isLive:
                                # Was in live list
                                if msgID:
                                    msg = await guild.get_channel(channel[0]).fetch_message(msgID[0])
                                    await msg.delete()
                                    self.database.RemoveEntry("TwitchMessages",
                                                              ["ServerID", "ChannelID", "MessageID"],
                                                              [user[0], channel[0], msgID[0]])
                else:
                    print("Did not get a successful response from twitch: " + str(resp.status))
        except Exception as e:
            print("**Hit exception in checkTwitch()**")
            print(type(e).__name__ + ' ' + str(e))

    @checkTwitch.before_loop
    async def before_checkTwitch(self):
        self.session = aiohttp.ClientSession()
        await self.bot.wait_until_ready()
        await self.__removeOldMessages()
        
    @checkTwitch.after_loop
    async def after_checkTwitch(self):
        if self.checkTwitch.is_being_cancelled() and not self.session.closed:
            await self.session.close()
            
    @commands.command(pass_context=True)
    async def addTwitch(self, ctx, name: str):
        if self.session:
            if self.oathExpiration < datetime.now():
                await self.__getOathToken()
            async with self.session.get('https://api.twitch.tv/helix/users?login=' + name, headers=self.headers) as resp:
                json = await resp.json()
                try:
                    if json['data']:
                        self.database.SetFields("Users", ["ServerID", "UserID"],
                                                [ctx.message.guild.id, ctx.message.author.id], ["Twitch"], [name])
                        await ctx.send("I set your twitch name to:  " + name)
                    else:
                        await ctx.send("I'm sorry but I cant find the username: " + name)
                    
                except KeyError:
                    print("Data not found in response")
                    print(json)
        else:
            await ctx.send("I'm still setting up")
        
    @commands.command(pass_context=True)
    async def removeTwitch(self, ctx):
        self.database.SetFields("Users", ["ServerID", "UserID"], [ctx.message.guild.id, ctx.message.author.id],
                                ["Twitch"], [""])
        await ctx.send("I removed your twitch username.")
        
    async def __getGameName(self, gameID):
        game_string = self.database.GetField("TwitchGameID", ["GameID"], [gameID], ["GameStr"])
        if not game_string:
            async with self.session.get('https://api.twitch.tv/helix/games?id=' + gameID, headers=self.headers) as resp:
                self.requests += 1
                if resp.status == 200:
                    json = await resp.json()
                    if json['data']:
                        name = json['data'][0]['name']
                        self.database.AddEntry("TwitchGameID", ["GameID", "GameStr"], [gameID, name], [], [])
                        return name
        else:
            return game_string[0]

    async def __getOathToken(self):
        async with self.session.post('https://id.twitch.tv/oauth2/token?client_id=' + self.clientID +'&client_secret=' + self.clientSecret + '&grant_type=client_credentials') as resp:
            if resp.status == 200:
                json = await resp.json()
                self.oathToken = json['access_token']
                self.oathExpiration = datetime.now() + timedelta(seconds=json['expires_in'])
                bearer = 'Bearer ' + self.oathToken
                self.headers = {'Client-ID': self.clientID, 'Authorization': bearer}
            else:
                print("Error in getting bearer token: " + str(resp.status))

            
    async def __removeOldMessages(self):
        for message in self.database.GetTable("TwitchMessages", ["ServerID", "ChannelID", "MessageID"]):
            try:
                msg = await self.bot.get_guild(message[0]).get_channel(message[1]).fetch_message(message[2])
                await msg.delete()
            except Exception as e:
                print(type(e).__name__ + str(e))   
            self.database.RemoveEntry("TwitchMessages", ["ServerID", "ChannelID", "MessageID"],
                                      [message[0], message[1], message[2]])
