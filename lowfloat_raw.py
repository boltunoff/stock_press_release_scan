
'''
webdriver proxy set up:
https://johnpatrickroach.com/2017/03/31/how-to-run-web-drivers-with-proxies-in-python/

includes Multiprocessing:
https://blog.miguelgrinberg.com/post/easy-web-scraping-with-python
from multiprocessing import Pool

def show_video_stats(options):
    pool = Pool(8)
    video_page_urls = get_video_page_urls()
    results = pool.map(get_video_data, video_page_urls)

https://gist.github.com/miguelgrinberg/5f52ceb565264b1e969a
http://stackoverflow.com/questions/26497722/scrape-multiple-pages-with-beautifulsoup-and-python
http://stackoverflow.com/questions/26727328/how-to-scrape-the-web-table-with-multiple-pages-using-r-or-python
http://stackoverflow.com/questions/10340290/python-beautifulsoup-looping-through-multiple-pages
http://www.kscottz.com/web-scraping-with-beautifulsoup-and-python/

'''

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import datetime
from random import choice
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os.path
import logging
import pandas as pd
import csv

#add generic log file location and name
#logging.basicConfig(filename='turotask_minivans.log', filemode="w", level=logging.INFO,format='%(asctime)s %(message)s')
    #Logging usage example:
    #logging.debug("This is a debug message")
    #logging.info("Informational message")
    #logging.error("An error has happened!")
#logging.info("Job started")

def driver_set():
    ua_list = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.82 Chrome/48.0.2564.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
    "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36"
    ]

    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.resourceTimeout"] = 15
    dcap["phantomjs.page.settings.loadImages"] = False
    dcap["phantomjs.page.settings.userAgent"] = choice(ua_list)

    driver = webdriver.PhantomJS(desired_capabilities=dcap)  # PhantomJs should be in the same dir of python.py file within project
    driver.set_window_size(1920,1080)
    return driver

def scrap_one_page(url):  # add argument url_now
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    # driver.close()
    # use the heirarchical nature of HTML structure to grab precisely the content that I am interested in
    # I will grab all of the elements that are within "li" tags and are also members of class "u-baseBottomMargin"

    base_page_data = soup.findAll('table')[0].findAll('tr')

    # Lowfloat last update:
    last_update = str(base_page_data[-1].text).lstrip('\n')
    print last_update
    # all pages to paginate thru
    paginate_pages = base_page_data[-2]
    # href links of all the pages:
    pages_href_links = base_page_data[-2].findAll('a')
    list_of_pages = []
    for i in pages_href_links:
        try:
            list_of_pages.append(int(str(i.text)))
        except:
            pass
    # building a nested dictionary
    low_float_dict = {}
        # <table border="1" class="stocks" width="798" style="border-collapse:collapse;">
    stocks_table = soup.find('table', {'class': 'stocks'})
    for i in stocks_table.findAll('tr'):
        try:
                # <tr><td class="tdi"><a href="http://finance.yahoo.com/q?s=DIT" target="_blank">DIT</a></td>
            ticker = i.find('a', {"target": "_blank"}).text
                # <td class="tdi" align="right">266K</td>
            ticker_float = i.find('td', {'align': 'right'}).text
            low_float_dict[ticker] = ticker_float
            # not writing last update to dictionary, instead will use it as a csv header
            #low_float_dict['Lowfloat updated'] = last_update
        except AttributeError:
            pass
    url_now = str(driver.current_url)
    #print low_float_dict
    #print url_now
    #print list_of_pages
    return low_float_dict, url_now, list_of_pages, last_update

def next_url(url_now):
    # finding page number from url
    url_list = url_now.split('/')
    next_page_num = str(int(url_list[-1]) + 1)
    next_url_str = '/'.join(url_list[:-1]) + '/' + next_page_num
    #print next_url_str
    return next_url_str

if __name__ == '__main__':

    driver = driver_set()
    url = "http://lowfloat.com/all/1"

    low_float_dict, url_now, list_of_pages, last_updated = scrap_one_page(url)

    # building dictionary from the initial list of pages = [1, ... ,10]
    for i, page in enumerate(list_of_pages):
        next_url_str = next_url(url_now)
        print "url_now received the loop > \n", url_now
        print "next_url to extract in the loop > \n", next_url_str
        next_low_float_dict, url_now, list_of_pages_loop, last_update = scrap_one_page(next_url_str)
        low_float_dict.update(next_low_float_dict)
        print 'Dict from the loop \n', low_float_dict
        print len(low_float_dict)
        print len(next_low_float_dict)
        #print 'url_now from the loop \n', url_now
        print 'List of pages initial \n', list_of_pages
        print 'List of pages from the loop \n', list_of_pages_loop

    # extracting data from the pages that are not covered in the initial list = [1,...,10]
    not_covered_pages = set(list_of_pages_loop) - set(list_of_pages)
    if list(not_covered_pages) != []:
        print 'Remaining pages to go thru: \n', list(not_covered_pages)
        for i, e in enumerate(list(not_covered_pages)):
            url_str_wo_page_num = '/'.join(url_now.split('/')[:-1])
            next_url_str = url_str_wo_page_num + '/' + str(list(not_covered_pages)[i])
            print 'next URL from not covered in loop > \n', next_url_str
            next_low_float_dict, url_now, list_of_pages_loop, last_update = scrap_one_page(next_url_str)
            # updating original dict with values of new extracted dictionary
            low_float_dict.update(next_low_float_dict)
            print 'Dict from the extra \n', low_float_dict
            print len(low_float_dict)
            print len(next_low_float_dict)
            # print 'url_now from the loop \n', url_now
            print 'List of pages 1st \n', list_of_pages
            print 'List of pages from the loop \n', list_of_pages_loop

    driver.close()

    # write dictionary to csv file
    # TODO: add a check on the existing csv file for header - last updated. If it it the same, don't start a program. Right after name=main
    with open('lowfloat_raw.csv','wb') as f:
        w = csv.writer(f)
        w.writerow(['Updated', last_update])
        w.writerows(low_float_dict.items())

    #http://lowfloat.com/all/1