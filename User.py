import discord
from discord.ext import commands
import os


class User(commands.Cog):
    def __init__(self, bot, database, soundboard):
        self.bot = bot
        self.database = database
        self.soundBoard = soundboard
        
    @commands.command(pass_context=True)
    async def admin(self, ctx, cmd: str, *params: str):
        val = self.database.GetFields("Users", ["ServerID", "UserID"], [ctx.message.guild.id, ctx.message.author.id],
                                      ["Admin"])
        if val and val[0][0] == "True":
            if cmd == 'add':
                if len(params) >= 3 and params[0] == "sb":
                    success = self.soundBoard.addCommand(ctx.message.guild.id, params[1], params[2], params[3:])
                    if success == 0:
                        await ctx.send("Added sb {}".format(params[1]))
                    elif success == 1:
                        await ctx.send("{} already exists as a command.".format(params[1]))
                    elif success == 2:
                        await ctx.send("{} does not exist.".format(params[2]))
                elif len(params) == 2 and params[0] == "admin":
                    if self.database.SetFields("Users", ["ServerID", "UserID"],
                                               [ctx.message.guild.id, self.__stripId(params[1])], ["Admin"], ["True"]):
                        await ctx.send("Added admin {}".format(params[1]))
                elif len(params) == 1 and params[0] == "holidayChannel":
                    if self.database.SetFields("BotChannels", ["ServerID", "ChannelID"],
                                               [ctx.message.guild.id, ctx.message.channel.id], ['Type'], ['Holiday']):
                        await ctx.send("Added this channel for holiday games!")
                elif len(params) == 1 and params[0] == "twitchChannel":
                    if self.database.SetFields("BotChannels", ["ServerID", "ChannelID"],
                                               [ctx.message.guild.id, ctx.message.channel.id], ['Type'], ['Twitch']):
                        await ctx.send("Added this channel for Twitch updates!")
            elif cmd == 'remove':
                if len(params) == 2 and params[0] == "sb":
                    if self.soundBoard.removeCommand(ctx.message.guild.id, params[1]):
                        await ctx.send("Removed sb {}".format(params[1]))
                elif len(params) == 2 and params[0] == "admin":
                    if self.database.SetFields("Users", ["ServerID", "UserID"],
                                               [ctx.message.guild.id, self.__stripId(params[1])], ["Admin"], ["False"]):
                        await ctx.send("Removed admin {}".format(params[1]))
                elif len(params) == 1 and params[0] == "holidayChannel":
                    if self.database.RemoveEntry("BotChannels", ["ServerID", "ChannelID", "Type"],
                                                 [ctx.message.guild.id, ctx.message.channel.id, "Holiday"]):
                        await ctx.send("Removed this channel from holiday games!")
                elif len(params) == 1 and params[0] == "twitchChannel":
                    if self.database.RemoveEntry("BotChannels", ["ServerID", "ChannelID", "Type"],
                                                 [ctx.message.guild.id, ctx.message.channel.id, "Twitch"]):
                        await ctx.send("Removed this channel from Twitch updates.")
            elif cmd == 'mute':
                if len(params) == 2 and params[0] == "sb":
                    if self.soundBoard.muteCommand(ctx.message.guild.id, params[1], "True"):
                        await ctx.send("Muted sb {}".format(params[1]))
                elif len(params) == 2 and params[0] == "user":
                    if self.database.SetFields("Users",  ["ServerID", "UserID"],
                                               [ctx.message.guild.id, self.__stripId(params[1])], ["Mute"], ["True"]):
                        await ctx.send("Muted user {}".format(params[1]))
            elif cmd == 'unmute':
                if len(params) == 2 and params[0] == "sb":
                    if self.soundBoard.muteCommand(ctx.message.guild.id, params[1], "false"):
                        await ctx.send("Unmuted sb {}".format(params[1]))
                elif len(params) == 2 and params[0] == "user":
                    if self.database.SetFields("Users", ["ServerID", "UserID"],
                                               [ctx.message.guild.id, self.__stripId(params[1])], ["Mute"], ["False"]):
                        await ctx.send("Unmuted user {}".format(params[1]))
            elif cmd == 'update':
                if len(params) >= 3 and params[0] == "whois":
                    if self.database.SetFields("Users", ["ServerID", "UserID"],
                                               [ctx.message.guild.id, self.__stripId(params[1])], ["Iam"],
                                               [self.__combine_str(params[2:])]):
                        await ctx.send("Updated user {}'s information".format(params[1]))
                elif len(params) >= 3 and params[0] == "sb":
                    if self.soundBoard.updateCommand(ctx.message.guild.id, params[1], params[2:]):
                        await ctx.send("Updated sb {}.".format(params[1]))
                    else:
                        await ctx.send("Could not find command {}.".format(params[1]))
            elif cmd == 'sbfiles':
                if len(params) == 0:
                    txt = "The available files for sb commands are: "
                    files = os.listdir("./Audio")
                    for file in files:
                        print(file)
                        if ".mp3" in file:
                            txt = txt + file + ", "
                    await ctx.send(txt)
            else:
                await ctx.send('Unknown Command')
        else:
            await ctx.send("You are not an Admin!")
        
    @commands.command(pass_context=True)
    async def iam(self, ctx, *name: str):
        if self.database.SetFields("Users", ["ServerID", "UserID"],  [ctx.message.guild.id, ctx.message.author.id],
                                   ["Iam"], [self.__combine_str(name)]):
            await ctx.send("I updated your information.")
        else:
            await ctx.send("Something went wrong and I couldn't add you.")
            
    @commands.command(pass_context=True)
    async def whois(self, ctx, person: discord.Member):
        value = self.database.GetFields("Users", ["ServerID", "UserID"], [ctx.message.guild.id, person.id], ["Iam"])
        if value and value[0][0]:
            await ctx.send(person.name + " is " + value[0][0] + ".")
        else:
            await ctx.send("I do not know who " + person.name + " is.")
            
    async def on_member_join(self, member):
        if not self.database.FieldExists("Users", ["ServerID", "UserID"], [member.guild.id, member.id]):
            print("Adding " + member.name)
            self.database.AddEntry("Users", ["ServerID", "UserID"], [member.guild.id, member.id],
                                   ["Admin", "Mute", "Iam"], ["False", "False", ""])
    
    async def on_server_join(self, server):
        for member in server.members:
            if not self.database.FieldExists("Users", ["ServerID", "UserID"], [server.id, member.id]):
                if server.owner.id == member.id:
                    admin = "True"
                else:
                    admin = "False"
                self.database.AddEntry("Users", ["ServerID", "UserID"], [server.id, member.id],
                                       ["Admin", "Mute", "Iam"], [admin, "False", ""])
                        
    def __stripId(self, user_id):
        return user_id[2:-1]
        
    def __combine_str(self, strings):
        name = ''
        for x in strings:
            name += x + " "
        return name.strip()
