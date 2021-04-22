#import required lib
import requests 
from bs4 import BeautifulSoup
import concurrent.futures
import time

#link = input("Enter url: ")
link="https://realpython.com/"

sitemap_lst=[]
title_tag=[]
h1_tag=[]
h2_tag=[]
img_tag=[]
a_tag=[]


def get_sitemap(lnk):
    sitemap_url= lnk+("sitemap.xml")
    sitemap_req= requests.get(sitemap_url)
    soup_1 = BeautifulSoup(sitemap_req.content, 'html.parser')
    #print(soup_1.prettify())
    t1=time.time()
    for link in soup_1.find_all("loc"):
            if link.text not in sitemap_lst:
                sitemap_lst.append(link.text)
                #print(link.text)

    if len(sitemap_lst)==0 :
        print("Sitemap is not available for this web-site.")
    else:
        #print("List of sitemap : ",sitemap_lst)
        print("Total sitemaps are ",len(sitemap_lst))

    t2=time.time()
    print(t2-t1)

get_sitemap(link)


sitemap_lst=sitemap_lst[:25]     #for time saving trim list


#webscraping
def webscrape(sitemap):

    #print(sitemaps)
    req=requests.get(sitemap)
    soup=BeautifulSoup(req.content,'html.parser')

    for title in soup.find_all("title"):
        if None in title:
            title_tag.append(None)    
        else:
            title_tag.append(title.text)

    for h1 in soup.find_all("h1"):
        if None in h1:
            h1_tag.append(None)    
        else:
            h1_tag.append(h1.text)
    
    for h2 in soup.find_all("h2"):
        if None in h2:
            h2_tag.append(None)    
        else:
            h2_tag.append(h2.text)
        
    for img in soup.find_all("img"):
        if img.has_attr('alt'):
            img_tag.append(img['alt'])

    for a in soup.find_all('a', href=True): 
        if None in a: 
            a_tag.append(None)
        else:
            a_tag.append(a['href'])


    
t5=time.time()
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(webscrape, sitemap_lst)

print("Total Title tags are ",len(title_tag))
print("Total h1 tags are ", len(h1_tag))
print("Total h2 tags are ",len(h2_tag))
print("Total img tags are ",len(img_tag))
print("Total a tags are ",len(a_tag))


#print("List of Title tags: ",title_tag) 
#print("List of h1 tags:",h1_tag)
#print("List of h2 tags:",h2_tag)
#print("List of img tags:",img_tag)
#print("List of a tag :", a_tag)
t6=time.time()
print("Total time requiered to scrape site,",t6-t5)
        



    