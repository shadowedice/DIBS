import urllib.request as ur
import re
from bs4 import BeautifulSoup, Tag

def mana_convert(text):
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
    else:
        return text

def card_check(card):
    try:
        page = ur.urlopen("http://gatherer.wizards.com/Pages/Card/Details.aspx?name=%s" % ur.quote(card)).read().decode('utf-8')
        return re.search('multiverseid=([0-9]*)', page).group(1)
    except AttributeError:
        print ("ERROR")
        return False
		
def card_text(card_id):
    link = "http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=%s" % card_id
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
                        ret += "%s" % mana_convert(fields['alt'])
                else:
                    ret += fields
            
        #Get all the text (This includes child text but it is ok)
        if(not value.find('div', class_="cardtextbox")):
            #find mana symbols and convert to text
            for alt in value.find_all('img'):
                ret += mana_convert(alt['alt'])
            if(not value.find('img')):
                ret += " %s" %value.get_text().strip()
        ret += "\n"
    return ret
    
def card_image(card_id):
    link = "http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=%s&type=card" % card_id
    imgname = "mtgcard.jpg"
    ur.urlretrieve(link, imgname)
    return imgname
    
def card_price(card):
    fmtName = ur.quote('+'.join(card.split(' ')), '/+')
    link = 'http://www.mtgstocks.com/cards/search?utf8=%E2%9C%93&print%5Bcard%5D={}&button='.format(fmtName)
    page = ur.urlopen(link).read()
    soup = BeautifulSoup(page, 'html.parser')
    
    if soup.find('td', class_="lowprice") is None:
        ret = "No pricing data found"
    else:
        ret = "---------------------------------\n"
        ret += "MTGStocks High: " + soup.find('td', class_="highprice").get_text() + "\n"
        ret += "MTGStocks Average: " + soup.find('td', class_="avgprice").get_text() + "\n"
        ret += "MTGStocks Low: " + soup.find('td', class_="lowprice").get_text() + "\n"
        ret += "---------------------------------"
    return ret
    