from discord.ext import commands
from discord import ChannelType
import asyncio
import random

class Holidays:
    def __init__(self, bot, database):
        self.bot = bot
        self.database = database
        
        #server, enabled, channel, message
        self.turkeys = []
        
        self.lock = asyncio.Lock()
        
    async def turkeyGame(self, server):  
        while server[1]:
            #check which channels are valid (do each time if permissions change)
            textChannels = []
            for chan in server[0].channels:
                if chan.type == ChannelType.text and chan.permissions_for(server[0].get_member(self.bot.user.id)).send_messages:
                    textChannels.append(chan)
                    
            #send turkey        
            server[3] = await self.bot.send_message(random.choice(textChannels), "Gobble gobble! :turkey:")
            sleepTime = random.randint(300,1800)
            timer = 0
            while timer < sleepTime and server[1]:
                await asyncio.sleep(30)
                timer += 30
            if server[3]:
                await self.bot.delete_message(server[3])
                server[3] = None
        
    @commands.command(pass_context=True)
    async def turkey(self, ctx):
        await self.lock.acquire()
        try:
            for server in self.turkeys:
                if server[3] and server[3].channel.id == ctx.message.channel.id:
                    #if they arent on the list add them
                    if not self.database.FieldExists("Holidays", ["ServerID", "UserID"], [ctx.message.server.id, ctx.message.author.id]):
                        self.database.AddEntry("Holidays", ["ServerID", "UserID"], [ctx.message.server.id, ctx.message.author.id], ["Turkeys"], ["0"])
                         
                    msg = "Gobble Gobble! {} just found a turkey!\n".format(ctx.message.author.name)
                    
                    for user in self.database.GetFields("Holidays", ["ServerID"], [ctx.message.server.id], ["UserID", "Turkeys"]):
                        turkey = int(user[1])
                        if user[0] == ctx.message.author.id:
                            turkey += 1
                            self.database.SetFields("Holidays", ["ServerID", "UserID"], [ctx.message.server.id, ctx.message.author.id], ["Turkeys"], [str(turkey)])
                        msg += "{}: {} x {}\n".format(server[0].get_member(user[0]).name, ":turkey:", turkey)
                        
                    await self.bot.send_message(server[2], msg)
                    
                    if server[3]:
                        await self.bot.delete_message(server[3])
                        server[3] = None
                    await self.bot.delete_message(ctx.message)
        finally:
            self.lock.release()
            
                
    @commands.command(pass_context=True)
    async def thanksgiving(self, ctx):
        if ctx.message.server.owner.id == ctx.message.author.id:
            foundServer = False
            for server in self.turkeys:
                if server[0].id == ctx.message.server.id:
                    if server[1]:
                        server[1] = False
                    else:
                        server[1] = True
                        server[2] = ctx.message.channel
                        await self.turkeyGame(server)
                    foundServer = True
            if not foundServer:
                server = [ctx.message.server, True, ctx.message.channel, None]
                self.turkeys.append(server)
                await self.turkeyGame(server)

    