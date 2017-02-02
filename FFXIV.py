from discord.ext import commands
import SoundEffect

class FFXIV:
    def __init__(self, bot):
        self.bot = bot
        self.userCommands = []
        self.getUserCommands()
            
    @commands.command(pass_context=True)
    async def ff(self, ctx, name : str):
        if name == 'forceupdate':
            self.getUserCommands()
            await self.bot.say("Updated FF Commands")
        else:
            for cmd in self.userCommands:
                if cmd[0] == name:
                    if cmd[1]:
                        if cmd[2]:
                            ret = cmd[1] % self.getFileCount('./VarFiles/' + cmd[2])
                        else:
                            ret = cmd[1]
                        await self.bot.say(ret)
                    try:
                        if cmd[3]:
                            await SoundEffect.playEffect(self.bot, ctx.message.author.voice_channel, cmd[3])
                    except AttributeError:
                        print("Error: Failed in %s callback" % cmd[0])
        
    def getFileCount(self, filename):
        try:
            file = open(filename, "r+")
            value = int(file.readline())
            value += 1
            file.seek(0)
        except FileNotFoundError:
            file = open(filename, "a+")
            value = 1
        file.write(str(value))
        file.close()
        return value
        
    def getUserCommands(self):
        self.userCommands.clear()
        with open("./Commands/userCommands.txt") as file:
            for line in file:
                self.userCommands.append([line.strip(), file.readline().strip(), file.readline().strip(), file.readline().strip()])
        
        
    