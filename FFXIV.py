from discord.ext import commands
import SoundEffect

class FFXIV:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def xanthe(self, ctx):
        ret = "Xanthe and his crazy puns are now at: %d" % self.getPunCount()
        await self.bot.say(ret)
        try:
            await SoundEffect.playEffect(self.bot, ctx.message.author.voice_channel, 'Level Down.mp3')
        except AttributeError:
            pass
        
    def getPunCount(self):
        try:
            file = open("punCount.txt", "r+")
            value = int(file.readline())
            value += 1
            file.seek(0)
        except FileNotFoundError:
            file = open("punCount.txt", "a+")
            value = 1
        file.write(str(value))
        file.close()
        return value
        
        
    