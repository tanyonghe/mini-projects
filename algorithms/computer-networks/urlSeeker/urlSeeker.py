########################
# Parallel Web Crawler #
# CS3103 Assignment 1D #
#          -           #
#     Tan Yong He      #
#      A0155401U       #
########################


from bs4 import BeautifulSoup
from urllib.parse import urlparse 
import multiprocessing
import os
import requests 
import time


''' Default Variables '''  # DO NOT CHANGE
DEFAULT_URL = "https://www.geeksforgeeks.org/"  # origin URL to crawl from
DEFAULT_OUTPUT = "crawled_links.txt"  # output file containing scraped links
DEFAULT_CRAWL_TIME = 60  # in seconds; a stopping criterion
DEFAULT_MAX_NUM_OF_VISITED_LINKS = 200  # additional stopping criterion besides time
DEFAULT_STOPPING_CRITERION = 2  # 1 for crawl time; 2 for number of links
DEBUG = False  # print debugging statements
CS3103 = True  # print CS3103 required information

''' User-defined Variables '''  # EDIT THIS IF REQUIRED
URL = ""
OUTPUT = ""
CRAWL_TIME = 0
MAX_NUM_OF_VISITED_LINKS = 0
STOPPING_CRITERION = 0
DEBUG = False


''' Set up web crawler variables for usage '''
if URL == "":
    URL = DEFAULT_URL
if OUTPUT == "":
    OUTPUT = DEFAULT_OUTPUT
if CRAWL_TIME == 0:
    CRAWL_TIME = DEFAULT_CRAWL_TIME
if MAX_NUM_OF_VISITED_LINKS == 0:
    MAX_NUM_OF_VISITED_LINKS = DEFAULT_MAX_NUM_OF_VISITED_LINKS
if STOPPING_CRITERION == 0:
    STOPPING_CRITERION = DEFAULT_STOPPING_CRITERION

''' Helper function to send a request to a given URL and return a list of scraped URLs in the response data '''
def retrieve_urls(url):
    retrieved_urls = list()
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')
        
        # For CS3103, print out visited web pages together with their server response timing in milliseconds
        if CS3103 == True:
            print("%s (%d milliseconds)"% (url, r.elapsed.total_seconds() * 1000))
        
        # Scrap all URLs in 'a href' elements from response data
        for row in soup.findAll('a'):
            retrieved_urls.append(row['href'])
            #print(row['href'])
        return retrieved_urls
    except:
        return -1

''' Worker function to crawl URLs in a given queue and add new URLs into the same queue ''' 
def crawl(crawled_dict, crawl_list, write_list):
    if DEBUG == True:
        print("Created a Crawl Worker with PID", os.getpid())

    while True:
        # Workers wait until there is something for them to do
        src_url = crawl_list.get(True)
        retrieved_urls = retrieve_urls(src_url)
        
        # Workers stop working once stopping criterion is met
        if STOPPING_CRITERION == 2 and len(crawled_dict) > MAX_NUM_OF_VISITED_LINKS:
            break;
        
        # Add valid URL to crawled dictionary if not already inside
        if retrieved_urls != -1 and src_url not in crawled_dict:
            write_list.put(src_url)
            crawled_dict[src_url] = 1
            for url in retrieved_urls:
                if not urlparse(url).netloc:
                    url = src_url + url
                if url not in crawled_dict:
                    crawl_list.put(url)
                    if DEBUG == True:
                        print("Worker with PID", os.getpid(), "scraped URL", url)
                        
        # Add invalid URL to crawled dictionary as a form of blacklist for future crawls
        elif retrieved_urls == -1 and src_url not in crawled_dict:
            crawled_dict[src_url] = 1

''' Worker function to write scraped URLs into a file '''      
def write(crawled_dict, crawl_list, write_list):
    while True:
        write_url = write_list.get(True)
        f = open(OUTPUT, "a+")
        f.write("%s\r\n" % write_url)
        f.close()
    
def main():
    # Welcome Message
    print("Starting up urlSeeker...")
    if CS3103 == True:
        print("CS3103: Visited web pages will be displayed together with the server response timing in milliseconds.")
    
    # Controls service process which holds Python objects and allows other processes to manipulate them using proxies (i.e. shared memory)
    manager = multiprocessing.Manager()
    
    # Keeps track of visited URLs and excludes them from future crawls
    crawled_dict = manager.dict()
    
    # Keeps track of URLs to be soon visited
    crawl_list = manager.Queue()
    crawl_list.put(URL)
    
    # Keeps track of URLs to be written into the output file
    write_list = manager.Queue()
    
    # 10 workers will run in parallel to crawl sites for more sites
    crawl_pool = multiprocessing.Pool(10, crawl, (crawled_dict, crawl_list, write_list))
    
    # 1 worker will oversee this queue and write in new distinct URLs
    write_pool = multiprocessing.Pool(1, write, (crawled_dict, crawl_list, write_list))
    
    # Buffer time for workers to start working
    time.sleep(5)
    
    # Workers will crawl sites until sleep is over
    if STOPPING_CRITERION == 1:
        time.sleep(CRAWL_TIME)
        print("Reached crawl time limit. Terminating in 5 seconds.")
        time.sleep(5)
    # Workers will crawl sites until it first passes the max number of visited links limit OR until no links are left to visit
    elif STOPPING_CRITERION == 2:
        while len(crawled_dict) < MAX_NUM_OF_VISITED_LINKS or crawl_list.qsize() == 0:
            #print("Number of links in queue:", crawl_list.qsize())
            #print("Number of visited links:", len(crawled_dict), "\r\n")
            time.sleep(1)
        # Buffer time for workers to stop working
        print("Number of visited links:", len(crawled_dict))
        print("Reached max number of visited links limit. Terminating in 5 seconds.")
        time.sleep(5)
        

if __name__ == '__main__':
    main()

    
