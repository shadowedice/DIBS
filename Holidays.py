import discord
from discord.ext import commands
from datetime import date
from datetime import datetime
from operator import itemgetter
import asyncio
import random

JANUARY = 1
NOVEMBER = 11
DECEMBER = 12
THANKSGIVING_DAY = 28
CHRISTMAS_DAY = 25
NYEVE_DAY = 31


class Holidays(commands.Cog):
    def __init__(self, bot, database):
        self.bot = bot
        self.database = database
        self.lock = asyncio.Lock()
        self.messages = []
        self.dynamicFactor = 3.0
        self.currentGame = ""

    async def startHoliday(self):
        while not self.bot.is_closed:
            if date.today().month == NOVEMBER:
                self.currentGame = "Thanksgiving"
                await self.thanksgivingGame()
            elif date.today().month == DECEMBER and date.today().day < CHRISTMAS_DAY:
                self.currentGame = "Christmas"
                await self.christmasGame()
            elif date.today().month == DECEMBER and date.today().day == NYEVE_DAY and datetime.now().hour >= 12:
                self.currentGame = "NewYears"
                await self.newYearsGame()
            else:
                self.currentGame = ""
            
            await asyncio.sleep(3600)
        
    async def newYearsGame(self):
        while self.currentGame == "NewYears" and not self.bot.is_closed:
            waitTime = 0
            # Just get the first channel, dont care about others
            for server in self.bot.servers:
                channel = self.database.GetField("BotChannels", ["ServerID", "Type"], [server.id, "Holiday"],
                                                 ["ChannelID"])
                if channel:
                    await self.bot.send_message(server.get_channel(channel[0]),
                                                "DRINK!!! :beer: :beers: :wine_glass: :champagne: :champagne_glass:")
                    
            if date.today().month == DECEMBER and datetime.now().hour >= 12:
                waitTime = random.randint(2700, 3600)
            if date.today().month == DECEMBER and datetime.now().hour >= 17:
                waitTime = random.randint(1200, 1800)
            if date.today().month == DECEMBER and datetime.now().hour >= 20:
                waitTime = random.randint(600, 900)
            if date.today().month == DECEMBER and datetime.now().hour >= 23:
                waitTime = random.randint(300, 400)
            if date.today().month == JANUARY:
                self.currentGame = ""
            await asyncio.sleep(waitTime)
            
    async def thanksgivingGame(self):
        pass
            
    @commands.command(pass_context=True)
    async def turkey(self, ctx, count):
        pass

    async def christmasGame(self):
        while self.currentGame == "Christmas" and not self.bot.is_closed:
            for server in self.bot.servers:
                channels = self.database.GetFields("BotChannels", ["ServerID", "Type"], [server.id, "Holiday"],
                                                   ["ChannelID"])
                if channels:
                    randVal = random.randint(0, 2)
                    msg = ""
                    if randVal == 0:
                        msg = "The grinch has left {} laying on the ground here!".format(":moneybag:" *
                                                                                         random.randint(2, 6))
                    elif randVal == 1:
                        msg = "The grinch has left {} laying on the ground here!".format(":gift:" *
                                                                                         random.randint(1, 4))
                    elif randVal == 2:
                        msg = "The grinch has left {} laying on the ground here!".format(":new_moon:" *
                                                                                         random.randint(6, 15))
                        
                    message = await self.bot.send_message(server.get_channel(random.choice(channels)[0]), msg)
                    self.messages.append(message)
            await asyncio.sleep(random.randint(1800, 3600))
            self.dynamicFactor = max(3.0, self.dynamicFactor - 0.05)
            
            for message in self.messages:
                await self.bot.send_message(message.channel, "It looks like the grinch found what he left behind...")
            self.messages.clear()
            
            if date.today().day >= CHRISTMAS_DAY:
                self.currentGame = ""
            
    async def acquireItem(self, ctx, count, item):
        if not await self.__checkForGame("Christmas"):
            return
        await self.lock.acquire()
        try:
            removeMsg = None
            for msg in self.messages:
                itemCount = msg.content.count(item)
                if msg.channel.id == ctx.message.channel.id and itemCount == count:
                    # if they arent on the list add them
                    if not self.database.FieldExists("Christmas", ["ServerID", "UserID"],
                                                     [ctx.message.server.id, ctx.message.author.id]):
                        self.database.AddEntry("Christmas", ["ServerID", "UserID"],
                                               [ctx.message.server.id, ctx.message.author.id],
                                               ["Bag", "Gift", "Coal", "OpenedBags", "TotalBags", "DibsGifts"],
                                               [0, 0, 0, 0, 0, 0])
                    
                    text = "{} recovered {} x {}!\n".format(ctx.message.author.name, item, itemCount)
                    
                    user = self.database.GetField("Christmas", ["ServerID", "UserID"],
                                                  [ctx.message.server.id, ctx.message.author.id],
                                                  ["Bag", "Gift", "Coal", "TotalBags"])
                    bags = user[0]
                    gifts = user[1]
                    coal = user[2]
                    totalBags = user[3]
                    if item == ":moneybag:":
                        bags += itemCount
                        totalBags += itemCount
                    elif item == ":gift:":
                        gifts += itemCount
                    elif item == ":new_moon:":
                        coal += itemCount
                    self.database.SetFields("Christmas", ["ServerID", "UserID"],
                                            [ctx.message.server.id, ctx.message.author.id],
                                            ["Bag", "Gift", "Coal", "TotalBags"], [bags, gifts, coal, totalBags])
                    text += self.__itemSummary(ctx.message.author.name, bags, gifts, coal)
                    await self.bot.say(text)
                    removeMsg = msg
                            
            if removeMsg:
                self.messages.remove(removeMsg)
                    
        finally:
            self.lock.release()
            
    @commands.command(pass_context=True)
    async def bags(self, ctx, count: int):
        await self.acquireItem(ctx, count, ":moneybag:")
            
    @commands.command(pass_context=True)
    async def gifts(self, ctx, count: int):
        await self.acquireItem(ctx, count, ":gift:")

    @commands.command(pass_context=True)
    async def coal(self, ctx, count: int):
        await self.acquireItem(ctx, count, ":new_moon:")
            
    @commands.command(pass_context=True)
    async def openBags(self, ctx, amount: int):
        if not await self.__checkForGame("Christmas"):
            return
        user = self.database.GetField("Christmas", ["ServerID", "UserID"],
                                      [ctx.message.server.id, ctx.message.author.id],
                                      ["Bag", "Gift", "Coal", "OpenedBags", "TotalBags"])
        if user:
            bags = user[0]
            if bags >= amount > 0:
                gifts = user[1]
                coal = user[2]
                openedBag = user[3]
                coalGain = 0
                giftGain = 0
                for x in range(amount):
                    factor = min(max(0.1, (openedBag / user[4])), 0.9)
                    if factor >= random.random():
                        coal += 1
                        coalGain += 1
                    else:
                        gifts += 2
                        giftGain += 2
                    openedBag += 1
                bags -= amount
                self.database.SetFields("Christmas", ["ServerID", "UserID"],
                                        [ctx.message.server.id, ctx.message.author.id],
                                        ["Bag", "Gift", "Coal", "OpenedBags"], [bags, gifts, coal, openedBag])
                msg = "{}! You managed to find :gift: x {} and :new_moon: x {}!\n".format(ctx.message.author.name,
                                                                                          giftGain, coalGain)
                msg += self.__itemSummary(ctx.message.author.name, bags, gifts, coal)
                await self.bot.say(msg)
            else:
                await self.bot.say("I'm afraid you don't have enough bags to open.")

    @commands.command(pass_context=True)
    async def convertBags(self, ctx, amount: int):
        if not await self.__checkForGame("Christmas"):
            return
        user = self.database.GetField("Christmas", ["ServerID", "UserID"],
                                      [ctx.message.server.id, ctx.message.author.id], ["Bag", "Gift", "Coal"])
        if user:
            bags = user[0]
            if bags >= amount > 0:
                gifts = amount + user[1]
                bags -= amount
                self.database.SetFields("Christmas", ["ServerID", "UserID"],
                                        [ctx.message.server.id, ctx.message.author.id],
                                        ["Bag", "Gift"], [bags, gifts])
                msg = "{}! :santa: used his magic to make :gift: x {}!\n".format(ctx.message.author.name, amount)
                msg += self.__itemSummary(ctx.message.author.name, bags, gifts, user[2])
                await self.bot.say(msg)
            else:
                await self.bot.say("I'm afraid you don't have enough bags to give.")
    
    @commands.command(pass_context=True)
    async def convertCoal(self, ctx, amount: int):
        if not await self.__checkForGame("Christmas"):
            return
        user = self.database.GetField("Christmas", ["ServerID", "UserID"],
                                      [ctx.message.server.id, ctx.message.author.id],
                                      ["Bag", "Gift", "Coal"])
        if user:
            coal = user[2]
            if coal >= amount > 0:
                if amount >= int(self.dynamicFactor):
                    newGifts = 0
                    gifts = user[1]
                    usedCoal = 0
                    while amount >= int(self.dynamicFactor):
                        newGifts += 1
                        gifts += 1
                        usedCoal += int(self.dynamicFactor)
                        amount -= int(self.dynamicFactor)
                        self.dynamicFactor += 0.1
                    coal -= usedCoal
                    self.database.SetFields("Christmas", ["ServerID", "UserID"],
                                            [ctx.message.server.id, ctx.message.author.id], ["Gift", "Coal"],
                                            [gifts, coal])
                    msg = "{}! :santa: used his magic to make :gift: x {} from :new_moon: x {}!\n".format(
                        ctx.message.author.name, newGifts, usedCoal)
                    msg += self.__itemSummary(ctx.message.author.name, user[0], gifts, coal)
                    await self.bot.say(msg)
                else:
                    await self.bot.say("I'm afraid you didn't give enough coal to make a gift.")
                    
            else:
                await self.bot.say("I'm afraid you don't have enough coal to give.")
    
    @commands.command()        
    async def coalMagic(self):
        if not await self.__checkForGame("Christmas"):
            return
        await self.bot.say(":santa: says it would take around :new_moon: x {} to make you one :gift:!".format(
            int(self.dynamicFactor)))
            
    @commands.command(pass_context=True)
    async def stealGifts(self, ctx, person: discord.Member):
        if not await self.__checkForGame("Christmas"):
            return
        user = self.database.GetField("Christmas", ["ServerID", "UserID"],
                                      [ctx.message.server.id, ctx.message.author.id], ["Bag", "Gift", "Coal"])
        if user:
            gifts = max(user[1] - 5, -2)
            self.database.SetFields("Christmas", ["ServerID", "UserID"], [ctx.message.server.id, ctx.message.author.id],
                                    ["Gift"], [gifts])
            msg = ":santa: Oh ho ho ho! We have a grinch here!\n"
            msg += "{}, you are going to need to give me some extra presents to make up for this!\n".format(
                ctx.message.author.name)
            msg += "You lost :gift: x {}!\n".format((user[1]-gifts))
            msg += self.__itemSummary(ctx.message.author.name, user[0], gifts, user[2])
            await self.bot.say(msg)

    @commands.command(pass_context=True)
    async def giveGifts(self, ctx, person: discord.Member, count: int):
        if not await self.__checkForGame("Christmas"):
            return
        donor = self.database.GetField("Christmas", ["ServerID", "UserID"],
                                       [ctx.message.server.id, ctx.message.author.id],
                                       ["Bag", "Gift", "Coal", "DibsGifts"])
        receiver = self.database.GetField("Christmas", ["ServerID", "UserID"], [ctx.message.server.id, person.id],
                                          ["Bag", "Gift", "Coal"])
        if donor and ctx.message.author.id != person.id:
            if donor[1] >= count > 0:
                donorGifts = donor[1] - count
                msg = ":santa: Oh ho ho! What a giving spirit! {} just gave {} :gift: x {}\n".format(
                    ctx.message.author.name, person.name, count)
                msg += self.__itemSummary(ctx.message.author.name, donor[0], donorGifts, donor[2])
                self.database.SetFields("Christmas", ["ServerID", "UserID"],
                                        [ctx.message.server.id, ctx.message.author.id], ["Gift"], [donorGifts])
                
                if receiver:
                    receiverGifts = receiver[1] + count
                    self.database.SetFields("Christmas", ["ServerID", "UserID"], [ctx.message.server.id, person.id],
                                            ["Gift"], [receiverGifts])
                    msg += self.__itemSummary(person.name, receiver[0], receiverGifts, receiver[2])
                else:
                    self.database.AddEntry("Christmas", ["ServerID", "UserID"], [ctx.message.server.id, person.id],
                                           ["Bag", "Gift", "Coal", "OpenedBags", "TotalBags", "DibsGifts"],
                                           [0, count, 0, 0, 0, 0])
                    msg += self.__itemSummary(person.name, 0, count, 0)
                await self.bot.say(msg)
                
                if person.id == self.bot.user.id:
                    dGifts = donor[3] + count
                    self.database.SetFields("Christmas", ["ServerID", "UserID"],
                                            [ctx.message.server.id, ctx.message.author.id], ["DibsGifts"], [dGifts])
                
            else:
                await self.bot.say("I'm sorry, but you don't have that many :gift: to give.")
                
    @commands.command(pass_context=True)
    async def christmasScore(self, ctx):
        text = ""
        users = self.database.GetFields("Christmas", ["ServerID"], [ctx.message.server.id],
                                        ["UserID", "Bag", "Gift", "Coal"])
        for user in sorted(users, key=itemgetter(2), reverse=True):
            bags = user[1]
            gifts = user[2]
            coal = user[3]
            text += self.__itemSummary(ctx.message.server.get_member(user[0]).name, bags, gifts, coal)
        await self.bot.say(text)
                
    def __itemSummary(self, name, bags, gifts, coal):
        return "{}: :moneybag: x {}, :gift: x {}, :new_moon: x {}\n".format(name, bags, gifts, coal)
        
    async def __checkForGame(self, game):
        if game == self.currentGame:
            return True
        else:
            await self.bot.say("I'm afraid it isn't the time of the year for that command")
            return False
