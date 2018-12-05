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
        self.dynamicFactor = 4.1
        
               
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
                    randVal = random.randint(0,2)
                    msg = ""
                    if randVal == 0:
                        msg = "The grinch has left {} laying on the ground here!".format(":moneybag:" * random.randint(2,6))
                    elif randVal == 1:
                        msg = "The grinch has left {} laying on the ground here!".format(":gift:" * random.randint(1,4))
                    elif randVal == 2:
                        msg = "The grinch has left {} laying on the ground here!".format(":new_moon:" * random.randint(6,15))
                        
                    message = await self.bot.send_message(server.get_channel(random.choice(channels)[0]), msg)
                    self.messages.append(message)
            #await asyncio.sleep(random.randint(1800,3600))
            await asyncio.sleep(random.randint(10,11))
            self.dynamicFactor = max(3.0, self.dynamicFactor - 0.01)
            
            for message in self.messages:
                await self.bot.send_message(message.channel, "It looks like the grinch found what he left behind...")
            self.messages.clear()
            
    async def acquireItem(self, ctx, count, item):
        await self.lock.acquire()
        try:
            removeMsg = None
            for msg in self.messages:
                itemCount = msg.content.count(item)
                if msg.channel.id == ctx.message.channel.id and itemCount == count:
                    #if they arent on the list add them
                    if not self.database.FieldExists("Christmas", ["ServerID", "UserID"], [ctx.message.server.id, ctx.message.author.id]):
                        self.database.AddEntry("Christmas", ["ServerID", "UserID"], [ctx.message.server.id, ctx.message.author.id], ["Bag", "Gift", "Coal", "OpenedBags", "TotalBags"], [0, 0, 0, 0, 0])
                    
                    text = "{} recovered {} x {}!\n".format(ctx.message.author.name, item, itemCount)
                    
                    for user in self.database.GetFields("Christmas", ["ServerID"], [ctx.message.server.id], ["UserID", "Bag", "Gift", "Coal", "TotalBags"]):
                        bags = user[1]
                        gifts = user[2]
                        coal = user[3]
                        totalBags = user[4]
                        if user[0] == ctx.message.author.id:
                            if item == ":moneybag:":
                                bags += itemCount
                                totalBags += itemCount
                            elif item == ":gift:":
                                gifts += itemCount
                            elif item == ":new_moon:":
                                coal += itemCount
                            self.database.SetFields("Christmas", ["ServerID", "UserID"], [ctx.message.server.id, ctx.message.author.id], ["Bag", "Gift", "Coal", "TotalBags"], [bags, gifts, coal, totalBags])
                        text += "{}: :moneybag: x {}, :gift: x {}, :new_moon: x {}\n".format(ctx.message.server.get_member(user[0]).name, bags, gifts, coal)
                    await self.bot.say(text)
                    removeMsg = msg
                            
            if removeMsg:
                self.messages.remove(removeMsg)
                    
        finally:
            self.lock.release()
            
    @commands.command(pass_context=True)
    async def bags(self, ctx, count : int):
        await self.acquireItem(ctx, count, ":moneybag:")
            
    @commands.command(pass_context=True)
    async def gifts(self, ctx, count : int):
        await self.acquireItem(ctx, count, ":gift:")

    @commands.command(pass_context=True)
    async def coal(self, ctx, count : int):
        await self.acquireItem(ctx, count, ":new_moon:")
            
    @commands.command(pass_context=True)
    async def openBags(self, ctx, amount : int):
        user = self.database.GetFields("Christmas", ["ServerID", "UserID"], [ctx.message.server.id, ctx.message.author.id], ["Bag", "Gift", "Coal", "OpenedBags", "TotalBags"])
        if user:
            bags = user[0][0]
            gifts = user[0][1]
            coal = user[0][2]
            if bags >= amount and bags > 0:
                openedBag = user[0][3]
                coalTotal = 0
                giftTotal = 0
                for x in range(amount):
                    factor = min(max(0.1, (openedBag / user[0][4])), 0.9)
                    if factor >= random.random():
                        coal += 1
                        coalTotal += 1
                    else:
                        gifts += 2
                        giftTotal += 2
                    openedBag += 1
                bags -= amount
                self.database.SetFields("Christmas", ["ServerID", "UserID"], [ctx.message.server.id, ctx.message.author.id], ["Bag", "Gift", "Coal", "OpenedBags"], [bags, gifts, coal, openedBag])
                msg = "{}! You managed to find :gift: x {} and :new_moon: x {}!\n".format(ctx.message.author.name, giftTotal, coalTotal)
                msg += "New totals: :moneybag: x {}, :gift: x {}, :new_moon: x {}\n".format(bags, gifts, coal)
                await self.bot.say(msg)
            else:
                await self.bot.say("I'm afraid you don't have enough bags to open.")
                
    
    @commands.command(pass_context=True)
    async def convertBags(self, ctx, amount : int):
        user = self.database.GetFields("Christmas", ["ServerID", "UserID"], [ctx.message.server.id, ctx.message.author.id], ["Bag", "Gift", "Coal"])
        if user:
            bags = user[0][0]
            if bags >= amount and bags > 0:
                gifts = amount + user[0][1]
                bags -= amount
                self.database.SetFields("Christmas", ["ServerID", "UserID"], [ctx.message.server.id, ctx.message.author.id], ["Bag", "Gift"], [bags, gifts])
                msg = "{}! :santa: used his magic to make :gift: x {}!\n".format(ctx.message.author.name, amount)
                msg += "New totals: :moneybag: x {}, :gift: x {}, :new_moon: x {}\n".format(bags, gifts, user[0][2])
                await self.bot.say(msg)
            else:
                await self.bot.say("I'm afraid you don't have enough bags to give.")
    
    @commands.command(pass_context=True)
    async def convertCoal(self, ctx, amount : int):
        user = self.database.GetFields("Christmas", ["ServerID", "UserID"], [ctx.message.server.id, ctx.message.author.id], ["Bag", "Gift", "Coal"])
        if user:
            coal = user[0][2]
            if coal >= amount and coal > 0:
                if amount >= int(self.dynamicFactor):
                    newGifts = 0
                    gifts = user[0][1]
                    usedCoal = 0
                    while amount >= int(self.dynamicFactor):
                        newGifts += 1
                        gifts += 1
                        usedCoal += int(self.dynamicFactor)
                        amount -= int(self.dynamicFactor)
                        self.dynamicFactor += 0.1
                    coal -= usedCoal
                    self.database.SetFields("Christmas", ["ServerID", "UserID"], [ctx.message.server.id, ctx.message.author.id], ["Gift", "Coal"], [gifts, coal])
                    msg = "{}! :santa: used his magic to make :gift: x {} from :new_moon: x {}!\n".format(ctx.message.author.name, newGifts, usedCoal)
                    msg += "New totals: :moneybag: x {}, :gift: x {}, :new_moon: x {}\n".format(user[0][0], gifts, coal)
                    await self.bot.say(msg)
                else:
                    await self.bot.say("I'm afraid you didn't give enough coal to make a gift.")
                    
            else:
                await self.bot.say("I'm afraid you don't have enough coal to give.")
    
    @commands.command()        
    async def coalMagic(self):
        await self.bot.say(":santa: says it would take around :new_moon: x {} to make you one :gift:!".format(int(self.dynamicFactor)))
            
    @commands.command(pass_context=True)
    async def stealGifts(self, ctx, person : discord.Member):
        user = self.database.GetFields("Christmas", ["ServerID", "UserID"], [ctx.message.server.id, ctx.message.author.id], ["Bag", "Gift", "Coal"])
        if user:
            gifts = max(user[0][1] - 5, -2)
            self.database.SetFields("Christmas", ["ServerID", "UserID"], [ctx.message.server.id, ctx.message.author.id], ["Gift"], [gifts])
            msg = ":santa: Oh ho ho ho! We have a grinch here!\n{}, you are going to need to give me some extra presents to make up for this!\n".format(ctx.message.author.name)
            msg += "You lost :gift: x {}!\n".format((user[0][1]-gifts))
            msg += "New totals: :moneybag: x {}, :gift: x {}, :new_moon: x {}\n".format(user[0][0], gifts, user[0][2])
            await self.bot.say(msg)

    @commands.command(pass_context=True)
    async def giveGifts(self, ctx, person : discord.Member, count : int):
        donor = self.database.GetFields("Christmas", ["ServerID", "UserID"], [ctx.message.server.id, ctx.message.author.id], ["Bag", "Gift", "Coal"])
        receiver = self.database.GetFields("Christmas", ["ServerID", "UserID"], [ctx.message.server.id, person.id], ["Bag", "Gift", "Coal"])
        if donor and ctx.message.author.id != person.id:
            if donor[0][1] >= count and count > 0:
                donorGifts = donor[0][1] - count
                msg = ":santa: Oh ho ho! What a giving spirit! {} just gave {} :gift: x {}\n".format(ctx.message.author.name, person.name, count)
                msg += "{} new totals: :moneybag: x {}, :gift: x {}, :new_moon: x {}\n".format(ctx.message.author.name, donor[0][0], donorGifts, donor[0][2])
                self.database.SetFields("Christmas", ["ServerID", "UserID"], [ctx.message.server.id, ctx.message.author.id], ["Gift"], [donorGifts])
                
                if receiver:
                    receiverGifts = receiver[0][1] + count
                    self.database.SetFields("Christmas", ["ServerID", "UserID"], [ctx.message.server.id, person.id], ["Gift"], [receiverGifts])
                    msg += "{} new totals: :moneybag: x {}, :gift: x {}, :new_moon: x {}\n".format(person.name, receiver[0][0], receiverGifts, receiver[0][2])
                else:
                    self.database.AddEntry("Christmas", ["ServerID", "UserID"], [ctx.message.server.id, person.id], ["Bag", "Gift", "Coal", "OpenedBags", "TotalBags"], [0, count, 0, 0, 0])
                    msg += "{} new totals: :moneybag: x {}, :gift: x {}, :new_moon: x {}\n".format(person.name, 0, count, 0)
                await self.bot.say(msg)
                
            else:
                await self.bot.say("I'm sorry, but you don't have that many :gift: to give.")
                    
                
                
        