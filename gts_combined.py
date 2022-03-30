# -*- coding: utf-8 -*-

from metaphone import doublemetaphone
from collections import Counter
from newspaper import Article
from googletrans import Translator
import stanza
import json
import sys

translator = Translator()

def hash_merged_names(merged_names):
    dmeta_merged_names = []
    for name, occurrences in merged_names:
        dmeta_name = doublemetaphone(name[0])
        dmeta_merged_names.append([dmeta_name,occurrences]) 
    return dmeta_merged_names

def is_name_equal(name1, name2):
    if doublemetaphone(name1)[0] == doublemetaphone(name2)[0] or (doublemetaphone(name1)[0] == doublemetaphone(name2)[1] and doublemetaphone(name1)[1] == doublemetaphone(name2)[0]):
        return 1
    else:
        return 0
    
def combine_duplicated_names(names):
    d = Counter(names)
    names_set = set(names)
    combined_names = []
    for name in names_set:
        combined_names.append([name, d[name]])   
    return combined_names

def phonetic_merge_names(names):
    names = combine_duplicated_names(names)
    already_merged = []

    for name, occurrences in names:
        added_to_existing = False
        for merged in already_merged:
            for potentially_similar in merged[0]:
                if is_name_equal(name, potentially_similar):
                    merged[1] += occurrences
                    added_to_existing = True
                    break
            if added_to_existing:
                break
        if not added_to_existing:
            already_merged.append([[name],occurrences])
    
    return already_merged

def merge_names(names):
    merged_names = phonetic_merge_names(names)
    return hash_merged_names(merged_names)

def extract(url):

    try:
        
        story = Article(url)
        story.download()
        story.parse()
        content = story.text
    except:
        print("This URL did not return a status code of 200. Try a different URL.")
        return
    output = translator.translate(content)

    translated_content = output.text

    nes = get_nes(translated_content)
    
    entities = {}
    entities["persons"] = []
    entities["locations"] = []
    entities["organizations"] = []

    for ne in nes:
        ne_dict = ne.to_dict()
        if ne_dict["type"] == "PERSON":
            entities["persons"].append(ne_dict["text"])
        if ne_dict["type"] == "GPE":
            entities["locations"].append(ne_dict["text"])
        if ne_dict["type"] == "ORG":
            entities["organizations"].append(ne_dict["text"])
            
    entities["persons"] = merge_names(entities["persons"])
    entities["locations"] = combine_duplicated_names(entities["locations"])
    entities["organizations"] = combine_duplicated_names(entities["organizations"])
    
    return entities    
            

def get_nes(input_text):
    stanza.download('en')
    nlp = stanza.Pipeline('en')
    output = nlp(input_text)
    return output.entities

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print ("Usage: Python gts.py <url>")
        print ("e.g: python gts.py http://example.com")
        sys.exit()
    else:
        entities = extract(sys.argv[1])
        if not entities:
            sys.exit()
        json_object = json.dumps(entities, indent = 4) 
        print(json_object)
