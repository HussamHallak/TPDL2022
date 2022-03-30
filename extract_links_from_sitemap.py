# -*- coding: utf-8 -*-
from usp.tree import sitemap_tree_for_homepage
import sys

def extract_links(url):
    tree = sitemap_tree_for_homepage(url)    
    urls = [page.url for page in tree.all_pages()]
    return urls

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print ("Usage: python extract_links_from_sitemap.py <url>")
        print ("e.g: python extract_links_from_sitemap.py https://www.aljazeera.com/")
        sys.exit()
    else:
        url = sys.argv[1]
        output = extract_links(url)
        #output = set(output)
        with open('links_from_sitemap.txt', 'a', encoding='utf-8') as output_file:
            for link in output:
                output_file.write(link + '\n')
        

