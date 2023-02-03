# -*- coding: utf-8 -*-
"""
Created on Sat Jul  2 08:19:52 2022

@author: Hussam
"""
import os
import sys
import time
from newspaper import Article   
import requests
import json

def split(links):
    exists = os.path.exists("output")
    if not exists:
        # Create a new directory because it does not exist
        os.makedirs("output")

    exists = os.path.exists("output_redo")
    if not exists:
        # Create a new directory because it does not exist
        os.makedirs("output_redo")

    for link in links:
        try:
            with requests.get(link, stream=True) as response:
                response = requests.get(link)
                if response.status_code == 200:
                    final_link = link
                else:
                    final_link = response.url 

                try:
                    story = Article(final_link)
                    story.download()
                    story.parse()
                    date_time = str(story.publish_date)
                    split_date = date_time.split()  
                    date = split_date[0]
                    # article = {"url": link, "final_url": final_link, "publish_date": date, "title": story.title, "text": story.text}
                    # with open("output/" + date + ".json", "a", encoding = 'utf-8') as output_file:
                    #     json.dump(article, output_file)
                    #     output_file.write("\n")
                    with open("output/" + date + ".txt", "a", encoding = 'utf-8') as output_file:
                        output_file.write(link + "\n")
                except:
                    print("The script was not able to extract published date. Moving the url to be crawled later.")
                    print("link: ", link)
                    print("status code: ", response.status_code)
                    print("final link: ", final_link)
                    with open("output_redo/" + "links_to_redo" + ".txt", "a", encoding = 'utf-8') as output_redo:
                            output_redo.write(link + "\n")            
                continue
        except:
            print("Connection refused by the server..")
            print("Sleeping for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("It's time to continue...")
        continue

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print ("Usage: Python split_by_date.py <file_name>")
        print ("e.g: python split_by_date.py input_file.txt")
        sys.exit()
    else:
        file_name = sys.argv[1]
        with open(file_name, "r", encoding = 'utf-8') as input_file:
            input_data = input_file.read()
            links = input_data.split("\n")
            del links[-1]
        split(links)
        