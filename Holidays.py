import discord
from discord.ext import commands
from datetime import date
import asyncio
import random

class Holidays:
    def __init__(self, bot, database):
        self.bot = bot
        self.database = database
        self.lock = asyncio.Lock()
        self.messages = []
        
               
    async def startHoliday(self):
        if date.today().month == 11:
            await self.thanksgivingGame()
        elif date.today().month == 12:
            await self.christmasGame()
        
            
    async def thanksgivingGame(self):
        pass
            
    @commands.command(pass_context=True)
    async def turkey(self, ctx, count):
        pass
    
        
    async def christmasGame(self):
        while date.today().month == 12 and date.today().day < 25:
            for server in self.bot.servers:
                channels = self.database.GetFields("HolidayChannels", ["ServerID"], [server.id], ["ChannelID"])
                if channels:
                    msg = await self.bot.send_message(server.get_channel(random.choice(channels)[0]), "The grinch has left {} bags laying on the ground here!".format(random.randint(2,5)))
                    self.messages.append(msg)
            await asyncio.sleep(random.randint(10,30))
            self.messages.clear()
            
            
    @commands.command(pass_context=True)
    async def bags(self, ctx, count : str):
        await self.lock.acquire()
        try:
            removeMsg = None
            for msg in self.messages:
                msgBags = msg.content[20:21]
                if msg.channel.id == ctx.message.channel.id and msgBags == count:
                    #if they arent on the list add them
                    if not self.database.FieldExists("Christmas", ["ServerID", "UserID"], [ctx.message.server.id, ctx.message.author.id]):
                        self.database.AddEntry("Christmas", ["ServerID", "UserID"], [ctx.message.server.id, ctx.message.author.id], ["Bag", "Gift", "Coal", "OpenedBags", "TotalBags"], ["0", "0", "0", "0", "0"])
                    
                    text = "{} recovered {} bags!\n".format(ctx.message.author.name, msgBags)
                    
                    for user in self.database.GetFields("Christmas", ["ServerID"], [ctx.message.server.id], ["UserID", "Bag", "Gift", "Coal", "TotalBags"]):
                        bags = user[1]
                        if user[0] == ctx.message.author.id:
                            bags = str(int(count) + int(user[1]))
                            totalBags = str(int(count) + int(user[4]))
                            self.database.SetFields("Christmas", ["ServerID", "UserID"], [ctx.message.server.id, ctx.message.author.id], ["Bag", "TotalBags"], [bags, totalBags])
                        text += "{}: :moneybag: x {}, :gift: x {}, :black_circle: x {}\n".format(ctx.message.server.get_member(user[0]).name, bags, user[2], user[3])
                    await self.bot.say(text)
                    removeMsg = msg
                            
            if removeMsg:
                self.messages.remove(removeMsg)
                    
        finally:
            self.lock.release()
            
    @commands.command(pass_context=True)
    async def openBags(self, ctx, count : int):
        user = self.database.GetFields("Christmas", ["ServerID", "UserID"], [ctx.message.server.id, ctx.message.author.id], ["Bag", "Gift", "Coal", "OpenedBags", "TotalBags"])
        bags = int(user[0][0])
        gifts = int(user[0][1])
        coal = int(user[0][2])
        if bags >= count:
            openedBag = int(user[0][3])
            for x in range(count):
                gifts += 2
                openedBag += 1
            bags -= count
            self.database.SetFields("Christmas", ["ServerID", "UserID"], [ctx.message.server.id, ctx.message.author.id], ["Bag", "Gift", "OpenedBags"], [str(bags), str(gifts), str(openedBag)])
            await self.bot.say("{}: :moneybag: x {}, :gift: x {}, :black_circle: x {}\n".format(ctx.message.author.name, bags, gifts, coal))
        else:
            await self.bot.say("I'm afraid you don't have enough bags to open.")
                
    @commands.command(pass_context=True)
    async def giveBags(self, ctx, count : int):
        user = self.database.GetFields("Christmas", ["ServerID", "UserID"], [ctx.message.server.id, ctx.message.author.id], ["Bag", "Gift"]) 
        if int(user[0][0]) <= count:
            gifts = str(count + int(user[0][1]))
            self.database.SetFields("Christmas", ["ServerID", "UserID"], [ctx.message.server.id, ctx.message.author.id], ["Bag", "Gift"], [str(int(user[0][0]) - count), gifts])
            await self.bot.say("{}! :santa: used his magic and you now have :gift: x {}!".format(ctx.message.author.name, gifts))
        else:
            await self.bot.say("I'm afraid you don't have enough bags to give.")
    
    @commands.command()        
    async def coalMagic(self):
        await self.bot.say(":santa: says it would take around :black_circle: x {} to make you one :gift:!".format(3))
    
    @commands.command(pass_context=True)
    async def giveCoal(self, ctx, count : int):
        user = self.database.GetFields("Christmas", ["ServerID", "UserID"], [ctx.message.server.id, ctx.message.author.id], ["Gift", "Coal"])
        coal =int(user[0][1]) 
        if coal >= count:
            newGifts = int(count / 3)
            gifts =  int(user[0][0]) + newGifts
            coal -= newGifts * 3
            self.database.SetFields("Christmas", ["ServerID", "UserID"], [ctx.message.server.id, ctx.message.author.id], ["Gift", "Coal"], [str(gifts), str(coal)])
            await self.bot.say("{}! :santa: used his magic and you now have :gift: x {} and :black_circle: x {}!".format(ctx.message.author.name, gifts, coal))
        else:
            await self.bot.say("I'm afraid you don't have enough coal to give.")
            
    @commands.command(pass_context=True)
    async def stealGifts(self, ctx, person : discord.Member):
        user = self.database.GetFields("Christmas", ["ServerID", "UserID"], [ctx.message.server.id, ctx.message.author.id], ["Gift"])
        victim = self.database.GetFields("Christmas", ["ServerID", "UserID"], [ctx.message.server.id, person.id], ["Gift"])
        gift = str(int(user[0][0]) + int(victim[0][0]))
        self.database.SetFields("Christmas", ["ServerID", "UserID"], [ctx.message.server.id, ctx.message.author.id], ["Gift"], [gift])
        self.database.SetFields("Christmas", ["ServerID", "UserID"], [ctx.message.server.id, person.id], ["Gift"], "0")
        await self.bot.say("{} stole all of {}'s gifts! What a grinch!".format(ctx.message.author.name, person.name))
            
        