from discord.ext import commands
import urllib.request as ur
import sqlite3

conn = sqlite3.connect('DIBS.db')
c = conn.cursor()

class SQL_Interaction:
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def plus_ten(self, searchString : str):
        c.execute('UPDATE user_points SET points = (points + 10) WHERE user = ?', (searchString,))
        conn.commit()

    @commands.command()
    async def search(self, searchString : str):
        c.execute('SELECT user, points FROM user_points WHERE user = ?', (searchString,))
        all_rows = c.fetchall()
        for row in all_rows:
            await self.bot.say(row)