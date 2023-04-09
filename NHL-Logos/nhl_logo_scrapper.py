from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as  uReq
import requests
import urllib.parse

urls = ['https://en.wikipedia.org/wiki/Category:National_Hockey_League_logos']

wiki = "https://en.m.wikipedia.org/wiki/"


print("itsok")

def get_club_name(string):
    name = string[5:len(string)]
    name = name.replace(".", "")
    retName = name[0:len(name)-7]
    return retName


for my_url in urls:
    all_links = []
    #data = data.encode('utf-8') # data should be bytes
    https = "https:"
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    
    page_soup = soup(page_html, "html.parser")
    containers = page_soup.findAll("div", {"class":"mw-category-group"})
    links = page_soup.select(".mw-category-group > ul > li > a")
    
    for link in links:
        new_link = "" + wiki + link.text
        new_link = new_link.replace(" ", "_")
        all_links.append(new_link)
                
                
    counter = 0
    for link in all_links:
       # print(all_links[counter])
        url = all_links[counter]
        url = urllib.parse.urlsplit(url)
        url = list(url)
        url[2] = urllib.parse.quote(url[2])
        url = urllib.parse.urlunsplit(url)
        uClient = uReq(url)
        link_html = uClient.read()
        uClient.close()
    
        page_soup = soup(link_html, "html.parser")
        
        div = page_soup.find_all("div", {"class":"fullImageLink"})
        imgUrl = div[0].a['href']
        r = requests.get(""+https+imgUrl) # create HTTP response object
        
        name = links[counter].text
        nLen = len(name)-1
        extension = name[nLen-2] + name[nLen-1] + name[nLen] 
        
        clubName = get_club_name(name)
        
        with open("{}.{}".format(clubName, extension),'wb') as f:
            #write the contents of the response (r.content)
            # to a new file in binary mode.
            f.write(r.content)
            print("finished writing")
            
        print(counter)
        counter+=1