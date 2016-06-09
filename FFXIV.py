from discord.ext import commands
import SoundEffect

class FFXIV:
    def __init__(self, bot):
        self.bot = bot
        self.xanthePuns = 0

    @commands.command(pass_context=True)
    async def xanthe(self, ctx):
        self.xanthePuns += 1
        ret = "Xanthe and his crazy puns are now at: %d" % self.xanthePuns
        await self.bot.say(ret)
        await SoundEffect.playEffect(self.bot, ctx.message.author.voice_channel, 'Level Down.mp3')
    