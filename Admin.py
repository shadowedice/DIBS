from discord.ext import commands
from SoundBoard import SoundBoard
import configparser

class Admin:
    def __init__(self, bot, soundBoard):
        self.bot = bot
        self.soundBoard = soundBoard
        self.userFile = 'userList.ini'
        self.userList = configparser.ConfigParser()
        self.userList.read(self.userFile)
        
    @commands.command(pass_context=True)
    async def admin(self, ctx, cmd : str, *params : str):
        if self.__checkAdmin(str(ctx.message.author.id)):
            if cmd == 'add':
                if len(params) >= 3 and params[0] == "sb":
                    self.soundBoard.addCommand(params[1], params[2], params[3:])
                elif len(params) == 2 and params[0] == "admin":
                    self.__addAdmin(self.__stripId(params[1]))
            elif cmd == 'remove':
                if len(params) == 2 and params[0] == "sb":
                    self.soundBoard.removeCommand(params[1])
                elif len(params) == 2 and params[0] == "admin":
                    self.__removeAdmin(self.__stripId(params[1]))
            elif cmd == 'mute':
                if len(params) == 2 and params[0] == "sb":
                    self.soundBoard.muteCommand(params[1], "True")
                elif len(params) == 2 and params[0] == "user":
                    self.__muteUser(self.__stripId(params[1]), "True")
            elif cmd == 'unmute':
                if len(params) == 2 and params[0] == "sb":
                    self.soundBoard.muteCommand(params[1], "false")
                elif len(params) == 2 and params[0] == "user":
                    self.__muteUser(self.__stripId(params[1]), "False")
            else:
                await self.bot.say('Unknown Command')
        else:
            await self.bot.say("You are not an Admin!")
            
    def __saveUsers(self):
        with open(self.userFile, 'w') as file:
            self.userList.write(file)
    
    def __addAdmin(self, userId):
        self.userList[userId] = {}
        self.userList[userId]['mute'] = "false"
        self.userList[userId]['admin'] = "true"
        self.__saveUsers()
    
    def __removeAdmin(self, userId):
        if(self.userList.has_section(userId)):
            self.userList[userId]['admin'] = "false"
            self.__saveUsers()
        
    def __muteUser(self, userId, mute):
        #Update userList info
        if not self.userList.has_section(userId):
            self.userList[userId] = {}
        self.userList[userId]['mute'] = mute
        self.__saveUsers()
        
        #Update soundboard muted users
        muteList = []
        for user in self.userList.sections():
            if self.userList[user].getboolean('mute'):
                muteList.append(user)
        self.soundBoard.updateMutedUsers(muteList)
        
    def __checkAdmin(self, userId):
        foundAdmin = False
        for user in self.userList.sections():
            if self.userList[user].getboolean('admin'):
                if user == userId:
                    return True
                else:
                    foundAdmin = True
        if foundAdmin:
            return False
        else:
            self.__addAdmin(userId)
            return True
    
    def __stripId(self, userId):
        return userId[2:-1]
            
    
            