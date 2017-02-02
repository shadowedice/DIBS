from discord.ext import commands
import SoundEffect

class SoundBoard:
    def __init__(self, bot):
        self.bot = bot
        self.soundCommands = []
        self.getSoundCommands()
            
    @commands.command(pass_context=True)
    async def sb(self, ctx, name : str):
        if name == 'forceupdate':
            self.getSoundCommands()
            await self.bot.say("Updated SB Commands")
        else:
            for cmd in self.soundCommands:
                if cmd[0] == name:
                    try:
                        if cmd[1]:
                            await SoundEffect.playEffect(self.bot, ctx.message.author.voice_channel, cmd[1])
                    except AttributeError:
                        print("Error: Failed in %s callback" % cmd[0])
        
    def getSoundCommands(self):
        self.soundCommands.clear()
        with open("./Commands/soundCommands.txt") as file:
            for line in file:
                self.soundCommands.append([line.strip(), file.readline().strip(), file.readline().strip(), file.readline().strip()])
        
        
    