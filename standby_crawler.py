#Created by Kevin Bernat 3/7/2016
#Standby Crawler
#Purpose: Crawls a specific site to get information about how much electricity
#certain appliances use when in standby mode.

import re
import bs4
import queue
import json
import sys
import csv
import pprint
import sqlite3

import utility

url = "http://standby.lbl.gov/summary-table.html"
def visit_page(url):

    request = utility.get_request(url)
    text =utility.read_request(request)
    soup = bs4.BeautifulSoup(text, "html5lib")

    #pp = pprint.PrettyPrinter()

    #prettyXML=soup.prettify() 
    #pp.pprint(prettyXML)

    d = {}
    tr_tag = soup.find_all("tr")
    for tag in tr_tag:
        th_tag = tag.find_all("th")   
        for electronic in th_tag:
            electronic = electronic.text  


        td_tag = tag.find_all("td")
        n = 0
        l = []
        for tag in td_tag:
            if n == 0:

                condition = tag.text

            if n <5 and n > 0:
                #Assuming one sleeps 8 hours a night, this is the amount that
                #would be saved by an individual per month.
                if n!=4:
                    kwh_per_month = round(float(tag.text)*8*30,3)
                    l.append(kwh_per_month)
                else:      
                    l.append(tag.text)

            n+= 1

        try:  

            d.setdefault(electronic,[])
            if l != []:
                d[electronic].append({condition:l})

        except UnboundLocalError:
            print("Not valid")
                

    print(d)   


    #db = sqlite3.connect('improvements.db')
    #c = db.cursor()
    with open("standby.csv", "wt") as standby:
        for key, value in d.items():
            for condition in value:
                for key2,value2 in condition.items():
                    #print((key, key2, condition[key2][0],condition[key2][1],
                        #condition[key2][2],condition[key2][3]))
                #with open("standby.csv", "wt") as standby:
                    writer = csv.writer(standby)
                    writer.writerow((key, key2, condition[key2][0],condition[key2][1],
                    condition[key2][2],condition[key2][3]))

                #r = c.execute("INSERT INTO standby VALUES (?,?,?,?,?,?)", 
                #    [key, key2, condition[key2][0],condition[key2][1],
                #    condition[key2][2],condition[key2][3]])

def go():
    visit_page(url)

if __name__=="__main__":

    ans = go()
    #ans = go(sys.argv[1])  