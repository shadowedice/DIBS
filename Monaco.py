import urllib.request as ur
import re
from bs4 import BeautifulSoup

def current_movies():
    page = ur.urlopen("http://www.cinemark.com/theatre-detail.aspx?node_id=430717&").read()
    soup = BeautifulSoup(page, 'html.parser')
     
    ret = ""
    for holder in soup.findAll('div', class_="holder"):
        strong = holder.find('strong')
        if strong is not None:
            ahref = strong.find('a')
            if ahref is not None:
                ret += holder.find('strong').find('a').get_text() + "\n"
         
    return ret