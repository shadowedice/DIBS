import urllib.request as ur
import re
from bs4 import BeautifulSoup
import time

def current_movies():
    page = ur.urlopen("http://www.cinemark.com/theatre-detail.aspx?node_id=430717&").read()
    soup = BeautifulSoup(page, 'html.parser')
    
    ret = "-------------------------------------------\n" 
    ret += "Monaco showings for: " + time.strftime("%d/%m/%Y") + "\n"
    ret += "-------------------------------------------\n" 
    for infoBox in soup.findAll('div', class_="info-box"):
        ret += "-" + infoBox.find('a').get_text() + "\n        "
        for showtime in infoBox.findAll('span', class_="theatreShowtimeSingle"):
            ret += showtime.get_text().strip() + " ";
        ret += "\n"
         
    return ret