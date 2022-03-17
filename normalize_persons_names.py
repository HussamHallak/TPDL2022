# -*- coding: utf-8 -*-

from metaphone import doublemetaphone
from collections import Counter

def hash_merged_names(merged_names):
    dmeta_merged_names = []
    for name, occurrences in merged_names:
        dmeta_name = doublemetaphone(name[0])
        dmeta_merged_names.append([dmeta_name,occurrences]) 
    return dmeta_merged_names

def is_name_equal(name1, name2):
    if doublemetaphone(name1)[0] == doublemetaphone(name2)[0] or doublemetaphone(name1)[0] == doublemetaphone(name2)[1] or doublemetaphone(name1)[1] == doublemetaphone(name2)[0]:
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

names = ["Hussam", "Hosam", "Hussien", "Hussam", "Ahmed", "Michael Nelson", "Michelle Nelson", "Ahmad", "Samira", "Emily"]
print(merge_names(names))



