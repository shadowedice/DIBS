from discord.ext import commands
import configparser
import SoundEffect

class SoundBoard:
    def __init__(self, bot):
        self.bot = bot
        self.filename = 'soundboard.ini'
        self.soundCommands = configparser.ConfigParser()
        self.soundCommands.read(self.filename)
        self.mutedUsers = []
            
    @commands.command(pass_context=True)
    async def sb(self, ctx, name : str):
        if name == "commands":
            ret = "My current command list is "
            for cmd in self.soundCommands.sections():
                ret += "**"+ cmd + "**, "
            await self.bot.say(ret)
        else:
            if str(ctx.message.author.id) in self.mutedUsers:
                await self.bot.say("You are currently muted.")
            else:
                for cmd in self.soundCommands.sections():
                    if cmd == name and not self.soundCommands[cmd].getboolean('mute'):
                        if self.soundCommands[cmd]['text']:
                            ret = self.soundCommands[cmd]['text']
                            if self.soundCommands[cmd]['count'] != "-1":
                                self.soundCommands[cmd]['count'] = str(int(self.soundCommands[cmd]['count'])+1)
                                self.__saveCommands()
                                ret = ret.format(self.soundCommands[cmd]['count']);
                            await self.bot.say(ret)
                        try:
                            await SoundEffect.playEffect(self.bot, ctx.message.author.voice_channel, self.soundCommands[cmd]['file'])
                        except AttributeError:
                            print("Error: Failed in %s callback" % cmd)
                    
    def __saveCommands(self):
        with open(self.filename, 'w') as file:
            self.soundCommands.write(file)
            
    def addCommand(self, name, file, params):
        self.soundCommands[name] = {}
        self.soundCommands[name]['file'] = file
        if len(params) > 0:
            self.soundCommands[name]['text'] = params[0]
        if len(params) > 1:
            self.soundCommands[name]['count'] = params[1]
        if len(params) > 2:
            self.soundCommands[name]['mute'] = params[2]
        self.__saveCommands()
        return True
        
    def removeCommand(self, name):
        if self.soundCommands.remove_section(name):
            self.__saveCommands()
            return True
        else:
            return False
        
    def muteCommand(self, name, mute):
        if self.soundCommands.has_section(name):
            self.soundCommands[name]['mute'] = mute
            self.__saveCommands()
            return True
        else:
            return False
    
    def updateMutedUsers(self, muteList):
        self.mutedUsers = muteList