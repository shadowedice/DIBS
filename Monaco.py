import urllib.request as ur
import re
from bs4 import BeautifulSoup, Tag
import time

def movie_type(mvtype):
    print(mvtype.strip())
    if 'Privé - Ages 21+' in mvtype:
        return 'Privé - Ages 21+'
    elif 'Digital Cinema' in mvtype:
        return 'Digital Cinema'
    else:
        return 'RealD 3D'

def current_movies(date):
    if date is '':
        date = time.strftime("%m/%d/%Y")
    url = "http://www.cinemark.com/theatre-detail.aspx?node_id=430717&showtime_date=%s" % date
    page = ur.urlopen(url).read()
    soup = BeautifulSoup(page, 'html.parser')
    
    ret = "**-------------------------------------------**\n" 
    ret += "**Monaco showings for: " + date + "**\n"
    ret += "**-------------------------------------------**\n" 
    #for infoBox in soup.findAll('div', class_="info-box"):
    #    ret += "**" + infoBox.find('a').get_text() + "**\n        "
    #    for showtime in infoBox.findAll('span', class_="theatreShowtimeSingle"):
    #        ret += showtime.get_text().strip() + " ";
    #    ret += "\n"
     
    for infoBox in soup.findAll('div', class_="info-box"):
        ret += "**" + infoBox.find('a').get_text() + "**"
        timeBox = infoBox.find('div', class_="time-box").find('ul')
        for child in timeBox.descendants:
            if isinstance(child, Tag):
                if child.name == 'strong':
                    ret += "\n     " + movie_type(child.text) + ":   "
                if child.has_attr('class'):
                    if child['class'][0] == 'theatreShowtimeSingle':
                        ret += " " + child.text.strip()
        ret += "\n"
        
    return ret