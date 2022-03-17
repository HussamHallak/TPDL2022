# -*- coding: utf-8 -*-
from boilerpy3 import extractors
from googletrans import Translator
import stanza
import json
import sys

translator = Translator()
extractor = extractors.ArticleExtractor()

def extract(url):

    try:
        content = extractor.get_content_from_url(url)
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
