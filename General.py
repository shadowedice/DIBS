from discord.ext import commands
import random


class General(commands.Cog):
    def __init__(self):
        pass

    @commands.command()
    async def roll(self, ctx, dice: str):
        # Rolls a dice in NdN format.
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Format has to be in NdN!')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)