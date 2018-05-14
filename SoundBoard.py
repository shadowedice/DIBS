from discord.ext import commands
import configparser
import SoundEffect
import os

class SoundBoard:
    def __init__(self, bot, database):
        self.bot = bot
        self.database = database
            
    @commands.command(pass_context=True)
    async def sb(self, ctx, name : str):
        if name == "commands":
            ret = "My current command list is "
            vals = self.database.GetFields("SoundBoard", ["ServerID"], [ctx.message.server.id], ["Name", "Mute"])
            for cmd in vals:
                if cmd[1] != "True":
                    ret += "**"+ cmd[0] + "**, "
            await self.bot.say(ret)
        else:
            mute = self.database.GetFields("Users", ["ServerID", "UserID"], [ctx.message.server.id, ctx.message.author.id], ["Mute"])
            if mute and mute[0][0] == "True":
                await self.bot.say("You are currently muted.")
            else:
                vals = self.database.GetFields("SoundBoard", ["ServerID", "Name"], [ctx.message.server.id, name], ["File", "Text", "Count", "Mute"])
                if vals and vals[0][3] != "True":
                    if vals[0][1]:
                        ret = vals[0][1]
                        if vals[0][2] != "-1":
                            self.database.SetFields("SoundBoard", ["ServerID", "Name"], [ctx.message.server.id, name], ["Count"], [str(int(vals[0][2])+1)])
                            ret = ret.format(vals[0][2])
                        await self.bot.say(ret)
                    try:
                        await SoundEffect.playEffect(self.bot, ctx.message.author.voice_channel, vals[0][0])
                    except AttributeError:
                        print("Error: Failed in %s callback" % cmd)
                        
            
    def addCommand(self, server, name, file, params):
        if self.database.FieldExists("SoundBoard", ["ServerID", "Name"], [server, name]):
            return 1
        files = os.listdir("./Audio")
        found = False
        for f in files:
            if f == file:
                found = True
        if not found:
            return 2
            
        fields = ["File", "Text", "Count", "Mute"]
        values = [file, "", "-1", "False"]
        if len(params) > 0:
            values[1] = params[0]
        if len(params) > 1:
            values[2] = params[1]
        if len(params) > 2:
            values[3] = params[2]
        self.database.AddEntry("SoundBoard", ["ServerID", "Name"], [server, name], fields, values)
        return 0
    
    def updateCommand(self, server, name, params):
        if not self.database.FieldExists("SoundBoard", ["ServerID", "Name"], [server, name]):
            return False
            
        fields = ["File", "Text", "Count", "Mute"]
        self.database.SetFields("SoundBoard", ["ServerID", "Name"], [server, name], fields[:len(params)], params)
        return True
        
    def removeCommand(self, server, name):
        if self.database.RemoveEntry("SoundBoard", ["ServerID", "Name"], [server, name]):
            return True
        else:
            return False
        
    def muteCommand(self, server, name, mute):
        if self.database.SetFields("SoundBoard", ["ServerID", "Name"], [server, name], ["Mute"], [mute]):
            return True
        else:
            return False
