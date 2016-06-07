import discord
from discord.ext import commands
import random
from bs4 import BeautifulSoup
import urllib.request as ur

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='$', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(description='Grab stock of your choice')
async def stock(name):
    """Grabs the stock graph of your choice"""
    #Insurance against typical Greg shenanigans
    if name.lower() == 'greg':
        await bot.say('Greg is currently valued at $0.00. How sad.')
        return
    
    url = 'http://finance.yahoo.com/lookup;_ylc=X3oDMTFzYjlmNnBpBGtleXcDYmxhaHoEbWlkA21lZGlhcXVvdGVzc2VhcmNoBHNlYwNnZXRxdW90ZXNidG4Ec2xrA2xvb2t1cA--?s={}'.format(name)

    #Let BeautifulSoup do its thang
    tickerCheck = ur.urlopen(url).read()
    soup = BeautifulSoup(tickerCheck, 'html.parser')
    if(soup.find('div', class_="error")):
        await bot.say('There is no market data for that ticker value.')

    url = 'http://finance.yahoo.com/q?s={}'.format(name)
    stock = ur.urlopen('http://finance.yahoo.com/q?s={}'.format(name)).read()
    soup = BeautifulSoup(stock, 'html.parser')
    nameData = soup.find('div', class_="title")
    companyName = nameData.find('h2').getText()
    priceData = soup.find('span', class_="time_rtq_ticker")
    currentPrice = priceData.getText()

    #Return a string with desired data
    ret = 'Grabbing the stock data for: {}! May the market be ever in your favor!\n{}:\nCurrently valued at: ${}'.format(name, companyName, currentPrice)
    return ret