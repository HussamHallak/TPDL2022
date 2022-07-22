# -*- coding: utf-8 -*-
"""
Created on Sat Jul  2 08:19:52 2022

@author: Hussam
"""
import os
import sys
from newspaper import Article   

def split(links):
    exists = os.path.exists("output")
    if not exists:
        # Create a new directory because it does not exist
        os.makedirs("output")
    for link in links:
        try:
            story = Article(link)
            story.download()
            story.parse()
            date_time = str(story.publish_date)
            split_date = date_time.split()  
            date = split_date[0]
            if date != "None":
                with open("output/" + date + ".txt", "a", encoding = 'utf-8') as output_file:
                    output_file.write(link + "\n")
        except:
            print("This URL did not return a status code of 200. Try a different URL.")
            print(link)
            
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
        