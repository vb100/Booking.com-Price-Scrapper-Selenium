import requests, re
from bs4 import BeautifulSoup

l = []

base_url = 'https://www.booking.com/searchresults.en-gb.html?label=gen173nr-1FCAEoggJCAlhYSDNiBW5vcmVmaIgBiAEBmAEZwgEKd2luZG93cyAxMMgBDNgBAegBAfgBC5ICAXmoAgM;sid=20c42c0b783aafadf5e96bb173c1c595;class_interval=1;dest_id=-2601889;dest_type=city;group_adults=2;group_children=0;label_click=undef;no_rooms=1;raw_dest_type=city;room1=A%2CA;sb_price_type=total;src=index;src_elem=sb;ss=London;ssb=empty;rows=15;offset='

def count_objects(base_url):
    r = requests.get(base_url + "00")
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    link_id = len(soup.find_all("a", {"class":"sr_pagination_link"}))
    link_text = (soup.find_all("a", {"class":"sr_pagination_link"})[link_id-1])
    return int(link_text.text)*15

number_of_objects = count_objects(base_url)

for page in range(0, number_of_objects+1, 15):
    r = requests.get(base_url + str(page))
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    all=soup.find_all("div",{"class":"sr_item"})
    print(page, "is in proccess")
    for item in all:
        d = {}
        d["Name of hotel"] = item.find("span", {"class":"sr-hotel__name"}).text.replace("\n", "")
        d["Description"] = item.find("div", {"class":"hotel_desc"}).text.replace("\n", "")
        
        #Collecting data bout stars: 1, 2, 3, 4, 5, no stars
        try:
            if item.find("svg", {"class":"-sprite-ratings_stars_5"}) != None:
                d["Stars"] = "5 stars"
            elif item.find("svg", {"class":"-sprite-ratings_stars_4"}) != None:
                d["Stars"] = "4 stars"
            elif item.find("svg", {"class":"-sprite-ratings_stars_3"}) != None:
                d["Stars"] = "3 stars"
            elif item.find("svg", {"class":"-sprite-ratings_stars_2"}) != None:
                d["Stars"] = "2 stars"
            elif item.find("svg", {"class":"-sprite-ratings_stars_1"}) != None:
                d["Stars"] = "1 star"
            else:
                d["Stars"] = "No stars"
        except:
            d["Stars"] = "No stars"
            
        #Collecting data bout price level
        try:
            if item.find("div", {"class":"sr_price_estimate__val5"}) != None:
                d["Price level"] = "Prices at this property are generally among the most expensive in the city."
            elif item.find("div", {"class":"sr_price_estimate__val4"}) != None:
                d["Price level"] = "Prices at this property are generally more expensive than other places in this city."
            elif item.find("div", {"class":"sr_price_estimate__val3"}) != None:
                d["Price level"] = "Prices at this property are average compared to other places in this city."
            else:
                d["Price level"] = "Quite cheap"
        except:
            d["Price level"] = "Quite cheap"    
            
        try:
            d["Transport"] = item.find("span", {"class":"pub_trans"}).text.replace("\n", "")
        except:
            d["Transport"] = "No info"
            
        if item.find("span", {"class":"review-score-badge"}) != None:
            d["Score"] = float((item.find("span", {"class":"review-score-badge"}).text.replace("\n", "")))
        else:
            d["Score"] = 0
            
        if item.find("span", {"class":"review-score-widget__subtext"}) != None:
            d["Reviews"] = float(item.find("span", {"class":"review-score-widget__subtext"}).text.replace("\n", "").replace(",", ".").rsplit(' ',1)[0])
        else:
            d["Reviews"] = 0

        l.append(d)
        
import pandas as pd
df = pd.DataFrame(l)

df.to_csv('Booking.com.Objects4.csv')