# -*- coding: utf-8 -*-
from usp.tree import sitemap_tree_for_homepage
import sys
import requests

def extract_links(url):
    tree = sitemap_tree_for_homepage(url)    
    urls = [page.url for page in tree.all_pages()]
    return urls

def get_redirects(links):
    urls = []
    for link in links:
        try:
            response = requests.get(link)
            #Capture redirects
            new_link = response.url
            urls.append(new_link)
        except:
            print("This URL did not return a status code of 200. Try a different URL.")
            print(link, "\n", new_link)
        
    return urls

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print ("Usage: python extract_links_from_sitemap.py <url> <file_name")
        print ("e.g: python extract_links_from_sitemap.py https://www.aljazeera.com/ aljazeera.txt")
        sys.exit()
    else:
        url = sys.argv[1]
        file_name = sys.argv[2]
        output_urls = extract_links(url)
        #output = get_redirects(output_urls)
        output = set(output_urls)
        with open(file_name, 'a', encoding='utf-8') as output_file:
            for link in output:
                output_file.write(link + '\n')