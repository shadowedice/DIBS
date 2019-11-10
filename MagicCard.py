from discord.ext import commands
from discord import File
import urllib.request as ur
from bs4 import BeautifulSoup, Tag
import re
import aiohttp
import io

MESSAGE_LIMIT = 1800


class MagicCard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cardName = ''
        self.cardId = -1

    def combine_str(self, strings):
        name = ''
        for x in strings:
            name += x + " "
        return name.strip()

    def mana_convert(self, text):
        if text == 'Blue':
            return "U"
        elif text == 'Black':
            return "B"
        elif text == 'Green':
            return "G"
        elif text == 'White':
            return "W"
        elif text == 'Red':
            return "R"    
        elif text == 'Variable Colorless':
            return "X"
        else:
            return text

    async def card_check(self):
        try:
            async with aiohttp.request('GET', "http://gatherer.wizards.com/Pages/Card/Details.aspx?name=%s" %
                                              ur.quote(self.cardName)) as resp:
                return re.search('multiverseid=([0-9]*)', await resp.text()).group(1)
        except AttributeError:
            return False

    async def card_text(self):
        link = "http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=%s" % self.cardId
        async with aiohttp.request('GET', link) as resp:
        
            soup = BeautifulSoup(await resp.read(), 'html.parser')
            ret = ""
            
            for link in soup.find_all('div', class_="row"):
                # Get the label ie Card Name:, Mana cost:, etc
                ret += "**" + link.find('div', class_="label").get_text().strip() + "**"
                
                # Get the values for the labels
                value = link.find('div', class_="value")
        
                # This case is for the card text and it requires special parsing
                for text in value.find_all('div', class_="cardtextbox"):
                    ret += "\n"
                    for fields in text.descendants:
                        if isinstance(fields, Tag):
                            if fields.has_attr('alt'):
                                ret += "%s" % self.mana_convert(fields['alt'])
                        else:
                            ret += fields
                    
                # Get all the text (This includes child text but it is ok)
                if not value.find('div', class_="cardtextbox"):
                    # find mana symbols and convert to text
                    for alt in value.find_all('img'):
                        ret += self.mana_convert(alt['alt'])
                    if not value.find('img'):
                        ret += " %s" % value.get_text().strip()
                ret += "\n"
            return ret
    
    async def card_image(self):
        link = "http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=%s&type=card" % self.cardId
        async with aiohttp.request('GET', link) as resp:
            return io.BytesIO(await resp.read())
        
    async def card_rulings(self):
        link = "http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=%s" % self.cardId
        async with aiohttp.request('GET', link) as resp:
        
            soup = BeautifulSoup(await resp.read(), 'html.parser')
            ret = [""]

            for link in soup.find_all('td', class_="rulingsText"):
                text = "-" + link.get_text().strip() + "\n"
                # If one single ruling is bigger than message limit
                if len(text) > MESSAGE_LIMIT:
                    ret[-1].append([text[i:i + MESSAGE_LIMIT] for i in range(0, len(text), MESSAGE_LIMIT)])
                # If multiple rulings are bigger than message limit
                elif len(ret[-1]) + len(text) > MESSAGE_LIMIT:
                    ret.append(text)
                else:
                    ret[-1] += text
            if ret[0] is "":
                ret[0] = "No rulings found for card: " + self.cardName
                
            return ret
        
    async def card_legality(self):
        link = "http://gatherer.wizards.com/Pages/Card/Printings.aspx?multiverseid=%s" % self.cardId
        async with aiohttp.request('GET', link) as resp:
        
            soup = BeautifulSoup(await resp.read(), 'html.parser')
            ret = ""
            
            for link in soup.find_all('tr', class_="cardItem"):
                column = link.find('td', class_="column1")
                # this avoids the top table
                if column is not None:
                    ret += "**" + link.find('td', class_="column1").get_text().strip() + "**"
                    ret += ": " + link.find('td', attrs={'style': 'text-align:center;'}).get_text().strip() + "\n"
            
            if ret is "":
                ret = "No legality found for card: " + self.cardName
                
            return ret
        
    @commands.command()
    async def mtg(self, ctx, *strings: str):
        self.cardName = self.combine_str(strings)
        self.cardId = await self.card_check()
        if self.cardId:
            reply = await self.card_text()
            img_name = self.cardName + ".png"
            await ctx.send(reply, file=File(await self.card_image(), img_name))
        else:
            await ctx.send("Could not find card: " + self.cardName)
            
    @commands.command()
    async def mtgtext(self, ctx, *strings: str):
        self.cardName = self.combine_str(strings)
        self.cardId = await self.card_check()
        if self.cardId:
            reply = await self.card_text()
            await ctx.send(reply)
        else:
            await ctx.send("Could not find card: " + self.cardName)
            
    @commands.command()
    async def mtgimage(self, ctx, *strings: str):
        self.cardName = self.combine_str(strings)
        self.cardId = await self.card_check()
        img_name = self.cardName + ".png"
        if self.cardId:
            await ctx.send(file=File(await self.card_image(), img_name))
        else:
            await ctx.send("Could not find card: " + self.cardName)
            
    @commands.command()
    async def mtgrulings(self, ctx, *strings: str):
        self.cardName = self.combine_str(strings)
        self.cardId = await self.card_check()
        if self.cardId:
            reply = await self.card_rulings()
            for msg in reply:
                await ctx.send(msg)
        else:
            await ctx.send("Could not find card: " + self.cardName)
            
    @commands.command()
    async def mtglegality(self, ctx, *strings: str):
        self.cardName = self.combine_str(strings)
        self.cardId = await self.card_check()
        if self.cardId:
            reply = await self.card_legality()
            await ctx.send(reply)
        else:
            await ctx.send("Could not find card: " + self.cardName)
