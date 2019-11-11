from discord.ext import commands
import discord
import asyncio
import os


class SoundBoard(commands.Cog):
    def __init__(self, bot, database):
        self.bot = bot
        self.database = database

    @commands.command(pass_context=True)
    async def sb(self, ctx, name: str):
        if name == "commands":
            ret = "My current command list is "
            values = self.database.GetFields("SoundBoard", ["ServerID"], [ctx.message.guild.id], ["Name", "Mute"])
            for cmd in values:
                if cmd[1] != "True":
                    ret += "**" + cmd[0] + "**, "
            await ctx.send(ret)
        else:
            mute = self.database.GetFields("Users", ["ServerID", "UserID"],
                                           [ctx.message.guild.id, ctx.message.author.id], ["Mute"])
            if mute and mute[0][0] == "True":
                await ctx.send("You are currently muted.")
            else:
                values = self.database.GetFields("SoundBoard", ["ServerID", "Name"], [ctx.message.guild.id, name],
                                                 ["File", "Text", "Count", "Mute"])
                if values and values[0][3] != "True":
                    if values[0][1]:
                        ret = values[0][1]
                        if values[0][2] != "-1":
                            self.database.SetFields("SoundBoard", ["ServerID", "Name"], [ctx.message.guild.id, name],
                                                    ["Count"], [values[0][2] + 1])
                            ret = ret.format(values[0][2])
                        await ctx.send(ret)
                    try:
                        voice = await ctx.message.author.voice.channel.connect()

                        voice.play(discord.FFmpegPCMAudio('./Audio/' + values[0][0]))
                        timer = 0
                        while voice.is_playing():
                            await asyncio.sleep(1)
                            timer += 1
                            if timer > 30:
                                break
                        await voice.disconnect()

                    except Exception as exc:
                        print(type(exc).__name__ + str(exc))

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

