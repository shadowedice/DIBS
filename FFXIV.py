from discord.ext import commands
import SoundEffect

class FFXIV:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def xanthe(self, ctx):
        ret = "Xanthe and his crazy puns are now at: %d" % self.getFileCount("punCount.txt")
        await self.bot.say(ret)
        try:
            await SoundEffect.playEffect(self.bot, ctx.message.author.voice_channel, 'Level Down.mp3')
        except AttributeError:
            print("Error: Failed in xanthe callback")
    @commands.command(pass_context=True)
    async def pam(self, ctx):
        ret = "Pam has meditated %d times now!" % self.getFileCount("meditationCount.txt")
        await self.bot.say(ret)
        try:
            await SoundEffect.playEffect(self.bot, ctx.message.author.voice_channel, 'Pam Sound.mp3')
        except AttributeError:
            print("Error: Failed in pam callback")
        
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
        
        
    