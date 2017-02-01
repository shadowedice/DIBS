from discord.ext import commands
import SoundEffect

class FFXIV:
    def __init__(self, bot):
        self.bot = bot
        self.userCommands = []
        self.getUserCommands()

    #@commands.command(pass_context=True)
    #async def xanthe(self, ctx):
    #    ret = "Xanthe and his crazy puns are now at: %d" % self.getFileCount("punCount.txt")
    #    await self.bot.say(ret)
    #    try:
    #        await SoundEffect.playEffect(self.bot, ctx.message.author.voice_channel, 'Level Down.mp3')
    #    except AttributeError:
    #        print("Error: Failed in xanthe callback")
    #@commands.command(pass_context=True)
    #async def pam(self, ctx):
    #    ret = "Pam has meditated %d times now!" % self.getFileCount("meditationCount.txt")
    #    await self.bot.say(ret)
    #    try:
    #        await SoundEffect.playEffect(self.bot, ctx.message.author.voice_channel, 'Pam Sound.mp3')
    #    except AttributeError:
    #        print("Error: Failed in pam callback")
    #@commands.command(pass_context=True)
    #async def yoji(self, ctx):
    #    ret = "Yoji has taken %d big dicks!" % self.getFileCount("yojiCount.txt")
    #    await self.bot.say(ret)
    #    try:
    #        await SoundEffect.playEffect(self.bot, ctx.message.author.voice_channel, 'yoji.mp3')
    #    except AttributeError:
    #        print("Error: Failed in yoji callback")
    #        
    #@commands.command(pass_context=True)
    #async def sloppy(self, ctx):
    #    try:
    #        await SoundEffect.playEffect(self.bot, ctx.message.author.voice_channel, 'sloppy.mp3')
    #    except AttributeError:
    #        print("Error: Failed in sloppy callback")
            
    @commands.command(pass_context=True)
    async def ff(self, ctx, name : str):
        for cmd in self.userCommands:
            if cmd[0] == name:
                if cmd[1]:
                    if cmd[2]:
                        ret = cmd[1] % self.getFileCount(cmd[2])
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
        with open("userCommands.txt") as file:
            for line in file:
                self.userCommands.append([line.strip(), file.readline().strip(), file.readline().strip(), file.readline().strip()])
        
        
    