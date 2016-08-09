from discord.ext import commands
import urllib.request as ur
from bs4 import BeautifulSoup, Tag
import re
import os

MESSAGE_LIMIT = 1800

class MagicCard:
    def __init__(self,bot):
        self.bot = bot
        self.cardName = ''
        self.cardId = -1

    def combine_str(self, strings):
        name = ''
        for x in strings:
            name += x + " "
        return name.strip()
        
    def mana_convert(self, text):
        if(text == 'Blue'):
            return "U"
        elif(text == 'Black'):
            return "B"
        elif(text == 'Green'):
            return "G"
        elif(text == 'White'):
            return "W"
        elif(text == 'Red'):
            return "R"    
        elif(text == 'Variable Colorless'):
            return "X"
        else:
            return text

    def card_check(self):
        try:
            page = ur.urlopen("http://gatherer.wizards.com/Pages/Card/Details.aspx?name=%s" % ur.quote(self.cardName)).read().decode('utf-8')
            return re.search('multiverseid=([0-9]*)', page).group(1)
        except AttributeError:
            print ("ERROR")
            return False
    
    		
    def card_text(self):
        link = "http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=%s" % self.cardId
        page = ur.urlopen(link).read()
        
        soup = BeautifulSoup(page, 'html.parser')
        ret = ""
        
        for link in soup.find_all('div', class_="row"):
            #Get the label ie Card Name:, Mana cost:, etc
            ret += "**" + link.find('div', class_="label").get_text().strip() + "**"
            
            #Get the values for the labels
            value = link.find('div', class_="value")
    
            #This case is for the card text and it requires special parsing
            for text in value.find_all('div', class_="cardtextbox"):
                ret += "\n"
                for fields in text.descendants:
                    if isinstance(fields, Tag):
                        if fields.has_attr('alt'):
                            ret += "%s" % self.mana_convert(fields['alt'])
                    else:
                        ret += fields
                
            #Get all the text (This includes child text but it is ok)
            if(not value.find('div', class_="cardtextbox")):
                #find mana symbols and convert to text
                for alt in value.find_all('img'):
                    ret += self.mana_convert(alt['alt'])
                if(not value.find('img')):
                    ret += " %s" %value.get_text().strip()
            ret += "\n"
        return ret
    
    def card_image(self):
        link = "http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=%s&type=card" % self.cardId
        imgname = self.cardId + ".jpg"
        ur.urlretrieve(link, imgname)
        return imgname
    
    def card_price(self):
        noPrice = "---------------------------------\n"
        noPrice += "No pricing data found\n"
        noPrice += "---------------------------------"
        fmtName = ur.quote('+'.join(self.cardName.split(' ')), '/+')
        link = 'http://www.mtgstocks.com/cards/search?utf8=%E2%9C%93&print%5Bcard%5D={}&button='.format(fmtName)
        try:
            page = ur.urlopen(link).read()
        except:
            return noPrice
            
        soup = BeautifulSoup(page, 'html.parser')
        if soup.find('td', class_="lowprice") is None:
            return noPrice
        else:
            ret = "---------------------------------\n"
            ret += "MTGStocks High: " + soup.find('td', class_="highprice").get_text() + "\n"
            ret += "MTGStocks Average: " + soup.find('td', class_="avgprice").get_text() + "\n"
            ret += "MTGStocks Low: " + soup.find('td', class_="lowprice").get_text() + "\n"
            ret += "---------------------------------"
        return ret
        
    def card_rulings(self):
        link = "http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=%s" % self.cardId
        page = ur.urlopen(link).read()
        
        soup = BeautifulSoup(page, 'html.parser')
        ret = []
        ret.append("")
        retIndex = 0
        
        for link in soup.find_all('td', class_="rulingsText"):
            text = "-" + link.get_text().strip() + "\n";
            #If one single ruling is bigger than message limit
            if len(text) > MESSAGE_LIMIT:
                ret[retIndex].append([text[i:i + MESSAGE_LIMIT] for i in range(0, len(text), MESSAGE_LIMIT)])
            #If multiple rulings are bigger than message limit
            elif len(ret[retIndex]) + len(text) > MESSAGE_LIMIT:
                ret.append("")
                retIndex += 1
                ret[retIndex] += text
            else:
                ret[retIndex] += text
        return ret
        
    def card_legality(self):
        link = "http://gatherer.wizards.com/Pages/Card/Printings.aspx?multiverseid=%s" % self.cardId
        page = ur.urlopen(link).read()
        
        soup = BeautifulSoup(page, 'html.parser')
        ret = ""
        
        for link in soup.find_all('tr', class_="cardItem"):
            column = link.find('td', class_="column1");
            #this avoids the top table
            if column is not None:
                ret += "**" + link.find('td', class_="column1").get_text().strip() + "**"
                ret += ": " + link.find('td', attrs={'style':'text-align:center;'}).get_text().strip() + "\n"
        
        
        
    @commands.command()
    async def mtg(self,*strings : str):
        self.cardName = self.combine_str(strings)
        self.cardId = self.card_check()
        if self.cardId:
            reply = self.card_text()
            reply += self.card_price()
            imgname = self.card_image()
            await self.bot.upload(imgname, content=reply)
            os.remove(imgname)
            
    @commands.command()
    async def mtgtext(self, *strings : str):
        self.cardName = self.combine_str(strings)
        self.cardId = self.card_check()
        if self.cardId:
            reply = self.card_text()
            await self.bot.say(reply)
            
    @commands.command()
    async def mtgimage(self, *strings : str):
        self.cardName = self.combine_str(strings)
        self.cardId = self.card_check()
        if self.cardId:
            imgname = self.card_image()
            await self.bot.upload(imgname)
            os.remove(imgname)
            
    @commands.command()
    async def mtgprice(self, *strings : str):
        self.cardName = self.combine_str(strings)
        self.cardId = self.card_check()
        if self.cardId:
            reply = self.card_price()
            await self.bot.say(reply)
            
    @commands.command()
    async def mtgrulings(self, *strings : str):
        self.cardName = self.combine_str(strings)
        self.cardId = self.card_check()
        if self.cardId:
            reply = self.card_rulings()
            for msg in reply:
                await self.bot.say(msg)
            
    @commands.command()
    async def mtglegality(self, *strings : str):
        self.cardName = self.combine_str(strings)
        self.cardId = self.card_check()
        if self.cardId:
            reply = self.card_legality()
            await self.bot.say(reply)