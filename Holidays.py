from discord.ext import commands
from discord import ChannelType
import asyncio
import random

class Holidays:
    def __init__(self, bot):
        self.bot = bot
        self.turkeyStatChan = None
        self.currentTurkey = None
        self.turkeyArray = []
        

        
    @commands.command(pass_context=True)
    async def turkey(self, ctx):
        if self.currentTurkey and self.currentTurkey.channel.id == ctx.message.channel.id:
            foundUser = False
            for user in self.turkeyArray:
                if user[0].id == ctx.message.author.id:
                    user[1] += 1
                    foundUser = True
            if not foundUser:
                self.turkeyArray.append([ctx.message.author, 1])
            
            msg = "Gobble Gobble! {} just found a turkey!\n".format(ctx.message.author.name)    
            for user in self.turkeyArray:
                msg += "{}: {}".format(user[0].name, ":turkey:" * user[1])
            
            await self.bot.send_message(self.turkeyStatChan, msg)
                
            
            await self.bot.delete_message(self.currentTurkey)
            self.currentTurkey = None
            await self.bot.delete_message(ctx.message)
                
    @commands.command(pass_context=True)
    async def thanksgiving(self, ctx):
        if ctx.message.server.owner.id == ctx.message.author.id:
            self.turkeyStatChan = ctx.message.channel
            while True:
                #find all text channels and add a turkey
                textChannels = []
                for chan in ctx.message.server.channels:
                    if chan.type == ChannelType.text:
                        textChannels.append(chan)
                self.currentTurkey = await self.bot.send_message(random.choice(textChannels), "Gobble gobble! :turkey:")
                
                #sleep until the next turkey is loose, kill old turkey
                await asyncio.sleep(random.randint(300,1800))
                if self.currentTurkey:
                    await self.bot.delete_message(self.currentTurkey)
                    self.currentTurkey = None