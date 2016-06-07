from bs4 import BeautifulSoup
import urllib.request as ur

def stock(name):
    """Grabs the stock graph of your choice"""
    #Insurance against typical Greg shenanigans
    if name.lower() == 'greg':
        return 'Greg is currently valued at $0.00. How sad.'

    url = 'http://finance.yahoo.com/q?s={}'.format(name)
    stock = ur.urlopen(url).read()
    soup = BeautifulSoup(stock, 'html.parser')
    nameData = soup.find('div', class_="title")
    if nameData is None:
        return 'There is no market data for that ticker value.'
    else:
        companyName = nameData.find('h2').getText()
        priceData = soup.find('span', class_="time_rtq_ticker")
        currentPrice = priceData.getText()
    
        #Return a string with desired data
        ret = 'Grabbing the stock data for: {}! May the market be ever in your favor!\n{}:\nCurrently valued at: ${}'.format(name.upper(), companyName, currentPrice)
        return ret