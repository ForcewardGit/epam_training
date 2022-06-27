""" A main module of a program. This module is executed by a user.
"""

### Parse given arguments ###
from arg_parse import parse_arguments
parse_arguments()

### Import necessary modules and/or their content ###
import sys
import json
import logging
from url_parse import RSSFeed
from constants import *


if __name__ =="__main__":
    ### In case when the user added --verbose argument, change the logging level ###
    if DEBUG_MODE:
        logging.basicConfig(level = logging.INFO)
    
    ### If the user wants to see the version ###
    if VERSION_FLAG:
        print(f"Version of a program: {VERSION}")

    ### Create a parser ###
    if RSS_URL:
        url_parser = RSSFeed()
    else:
        sys.exit()

    ### If the parser is valid (i.e the url is 'parsable'), continue parsing ###
    if url_parser.valid and not JSON_FLAG:
        ## Create items and let the user see the title of a feed ##
        items = url_parser.parse_items()
        logging.info("Starting to print parsed objects...")
        print(f"\nFeed: {url_parser.title}\n\n{'-'*120}\n")

        ## For each item, print out its info ###
        for item in items:
            if item.valid:
                print(f"Title: {item.title}")
                print(f"Link: {item.link}")
                print(f"Description: {item.description}")
                if item.extra_links:
                    print("  Links inside the description:")
                    for i in range(len(item.extra_links)):
                        print(f"    [{i}] {item.extra_links[i]}")
                if item.media:
                    print(f"Media: {item.media}")
                print(f"Date: {item.date}")
            else:
                print("Invalid item")

            print("\n", "-" * 120, "\n")

            logging.info("Printing has finished!")
        
        if not items:
            print("There are no items in a given feed :(")

    elif url_parser.valid and JSON_FLAG:
        ## Parse items and create a dictionary to store the rss info (title, items, ...) ##
        items = url_parser.parse_items()
        logging.info("Starting to print parsed objects in json format...")
        rss_info = {}
        rss_info["Feed"] = url_parser.title
        rss_info["items"] = []

        ## Create a dictionary and add it to `rss_info`'s items ##
        for item in items:
            if item.valid:
                item_dict = {}
                item_dict["Title"] = item.title
                item_dict["Link"] = item.link
                item_dict["Description"] = item.description
                if item.extra_links:
                    item_dict["ExtraLinks"] = item.extra_links
                if item.media:
                    item_dict["Media"] = item.media
                item_dict["Date"] = item.date
                
                rss_info["items"].append(item_dict)

            else:
                rss_info["items"].append("Invalid item")
        
        ## Print the JSON representation of a result ##
        print(json.dumps(rss_info, indent = 4, ensure_ascii=False))
        
        logging.info("Printing has finished!")
        