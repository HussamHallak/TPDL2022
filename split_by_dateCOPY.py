# -*- coding: utf-8 -*-
"""
Created on Sat Jul  2 08:19:52 2022

@author: Hussam
"""
import os
import sys
from newspaper import Article   

def split(link):
        try:
            story = Article(link)
            story.download()
            story.parse()
            date_time = str(story.publish_date)
            title = story.title
            split_date = date_time.split()  
            date = split_date[0]
            print(title)
            print(story.publish_date)
            print("------------------")
        except:
            print("This URL did not return a status code of 200. Try a different URL.")
            print(link)

if __name__ == "__main__":
        link = "https://www.arabnews.com/middle-east/powerful-s-sudanese-military-leader-dies"
        split(link)
        link = "https://www.arabnews.com/tags/us-drug-enforcement-administration"
        split(link)
        link = "https://www.arabnews.com/tags/transit-flights"
        split(link)
        link = "https://www.arabnews.com/tags/motorbike-taxi"
        split(link)
        link = "https://www.arabnews.com/tags/payfort"
        split(link)
        link = "https://www.arabnews.com/tags/kitaf"
        split(link)   