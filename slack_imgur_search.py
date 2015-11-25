#!/usr/bin/env python
""" Searches for all the imgur links in a given slack channel or
    private conversation.
    
    To use:
    1) Replace the API_KEY below with your API_KEY, which may be obtained
    at `https://api.slack.com/web`
    2) Replace CHANN_NAME with the channel or conversation name that you
    wish to search
    
    """

import requests
import json
import re

API_KEY = "xxxx-xxxx-xxxx-xxxx-xxxx"
CHANN_NAME = "general"

SEARCH_STR = "http:.+imgur.com.+"
RESULTS_FILE = "slack_search.txt"

query = ("https://slack.com/api/search.all? " +
         "token=" + API_KEY + "&query=" + SEARCH_STR + " in:" + CHANN_NAME)

def extract_links(results):
    messages = results['messages']['matches']
        
        for msg in messages:
            # extract imgur link from rest of message
            try:
                l = re.findall('<' + SEARCH_STR + '>', msg['text'])
                    links.append(l[0][1:-1])
                except:
                    pass
    return links

def make_query(querystr):
    r = requests.get(querystr)
        return json.loads(r.content)


# get total number of pages
r_json = make_query(query)
pages = r_json['messages']['pagination']['page_count']

print "Found", pages, "pages of results"

# TODO check headers and response code (r.status_code, r.headers)


# extract list of links from results
links = []
for p in range(1,pages):
    r = make_query(query + "&page=" + str(p))
        links = links + extract_links(r)


# check for duplicate images
links = list(set(links))

print "Found a total of ", len(links), " results"

# export to csv
if len(links) != 0:
    with open(RESULTS_FILE, 'wb') as outfile:
        for l in links:
            outfile.write("%s\n" % l)
        print "Wrote to file", RESULTS_FILE
