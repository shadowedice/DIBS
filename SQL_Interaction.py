from discord.ext import commands
from pathlib import Path
import discord
import urllib.request as ur
import sqlite3
import os

conn = sqlite3.connect('DIBS.db')
sqlDB = conn.cursor()

class SQL_Interaction:
    def __init__(self,bot):
        self.bot = bot
        self.changePointsUser = ""
    
    @commands.command()
    async def setup_sql(self):
        
        #   This command has built-in duplication prevention methods so it can be run multiple
        #   times on one server without fear of redundant data input
        
        sqlDB.execute('''CREATE TABLE IF NOT EXISTS user_data (serverID, user, points, admin)''')
        sqlDB.execute('''CREATE TABLE IF NOT EXISTS sounds_data (serverID, soundName, soundPath)''')
        conn.commit()
        
        for curServer in self.bot.servers:
            for curMember in curServer.members:
                
                # Check if user is already in the database for this server
                sqlDB.execute('SELECT serverID FROM user_data WHERE user = ?', (curMember.name,))
                all_rows = sqlDB.fetchall()
                newUser = True
                for row in all_rows:
                    if row[0] == curServer.id:
                        newUser = False
                
                if (newUser):
                    if curMember == curServer.owner:
                        sqlDB.execute("INSERT INTO user_data (serverID, user, points, admin) VALUES (?, ?, 200, 1)", (curServer.id, curMember.name,))
                    else:
                        sqlDB.execute("INSERT INTO user_data (serverID, user, points, admin) VALUES (?, ?, 100, 0)", (curServer.id, curMember.name,))
            
        conn.commit()
        
    def isInt(self, inValue):
        try: 
            int(inValue)
            return True
        except ValueError:
            return False

    ## DATABASE READING FUNCTIONS
    
    @commands.command()
    async def search(self, searchString : str):
        sqlDB.execute('SELECT points FROM user_data WHERE user = ?', (searchString,))
        all_rows = sqlDB.fetchall()
        for row in all_rows:
            await self.bot.say(row[0])
    
    @commands.command()
    async def points_board(self):
        for row in sqlDB.execute('SELECT user, points FROM user_data ORDER BY points'):
            await self.bot.say(row)
    
    ## DATABASE WRITING FUNCTIONS
    
    @commands.command()
    async def manual_points(self, searchString : str):
        await self.bot.say("You are attempting to change %s's Dib-dab total.  Please type '$new_points ' followed by the desired Dib-dab total for %s."\
        % (searchString, searchString,))
        self.changePointsUser = searchString

    @commands.command()
    async def new_points(self, searchString : str):
        
        # Allow only if following manual_points command
        if self.changePointsUser == "":
            await self.bot.say("Use the $manual_points command first to designate a target user.")
            return
        
        if self.isInt(searchString):
            sqlDB.execute('UPDATE user_data SET points = ? WHERE user = ?', (int(searchString), self.changePointsUser,))
        else:
            await self.bot.say("Please enter in an integer.")
        
        conn.commit()
        
        # Verify that the data was entered correctly
        sqlDB.execute('SELECT points FROM user_data WHERE user = ?', (self.changePointsUser,))
        all_rows = sqlDB.fetchall()
        for row in all_rows:
            await self.bot.say("%s's new point value is: %s" % (self.changePointsUser, row[0]))

        self.changePointsUser = ""
        
    @commands.command()
    async def plus_ten(self, searchString : str):
        sqlDB.execute('UPDATE user_data SET points = (points + 10) WHERE user = ?', (searchString,))
        conn.commit()

    @commands.command()
    async def minus_ten(self, searchString: str):
        sqlDB.execute('UPDATE user_data SET points = (points - 10) WHERE user = ?', (searchString,))
        conn.commit()