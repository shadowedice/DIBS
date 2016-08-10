from discord.ext import commands
import urllib.request as ur
import datetime as dt
from bs4 import BeautifulSoup, Tag

class Monaco:
    def __init__(self, bot):
        self.bot = bot
        
    def movie_type(self, mvtype):
        if 'Privé - Ages 21+' in mvtype:
            return 'Privé - Ages 21+'
        elif 'Digital Cinema' in mvtype:
            return 'Digital Cinema'
        else:
            return 'RealD 3D'
            
    def getDate(self, date):
        today = dt.date.today()
        day = today + dt.timedelta((date-today.weekday()) % 7)
        return day.strftime("%m/%d/%Y")

    @commands.command()
    async def monaco(self, date : str):
        day = date.lower()
        days = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
        #handle illegal input and entering days of the week
        if day in days:
            date = self.getDate(days.index(day))
        else:
            try:
                dt.datetime.strptime(date,"%m/%d/%Y")
            except ValueError:
                await self.bot.say("Enter date in m/d/yyyy format or enter day of the week.")
                return
        url = "http://www.cinemark.com/theatre-detail.aspx?node_id=430717&showtime_date=%s" % date
        page = ur.urlopen(url).read()
        soup = BeautifulSoup(page, 'html.parser')
        
        ret = "**-------------------------------------------**\n" 
        ret += "**Monaco showings for: " + date + "**\n"
        ret += "**-------------------------------------------**\n" 
         
        for infoBox in soup.findAll('div', class_="info-box"):
            ret += "**" + infoBox.find('a').get_text() + "**"
            timeBox = infoBox.find('div', class_="time-box").find('ul')
            for child in timeBox.descendants:
                if isinstance(child, Tag):
                    if child.name == 'strong':
                        ret += "\n     " + self.movie_type(child.text) + ":   "
                    if child.has_attr('class'):
                        if child['class'][0] == 'theatreShowtimeSingle':
                            ret += " " + child.text.strip()
            ret += "\n"
            
        await self.bot.say(ret)
