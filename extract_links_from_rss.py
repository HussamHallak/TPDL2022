# -*- coding: utf-8 -*-
import feedparser
import time
import sys

def get_links_from_rss(url):
    links = []
    feed = feedparser.parse(url)
    for i in range(len(feed.entries)):
        links.append(feed.entries[i].link)
    return links

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print ("Usage: python extract_links_from_rss.py <url> <number of runs> <delay in hours>")
        print ("e.g: python extract_links_from_rss.py https://www.aljazeera.com/xml/rss/all.xml 3 1")
        sys.exit()
    else:
        url = sys.argv[1]
        runs = int(sys.argv[2])
        delay = float(sys.argv[3])
        output = []
        while(runs !=0):
            print("Running")
            links = get_links_from_rss(url)
            output = output + links
            runs = runs - 1            
            if runs == 0:
                break;
            print("Remaining Runs:", runs)
            print("Waiting for next run..")
            time.sleep(delay * 3600)
            
        output = set(output)
        with open('links_from_rss.txt', 'a') as output_file:
            for link in output:
                output_file.write(link + '\n')
                
print("Done!")