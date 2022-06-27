""" Module that handles the parsing of a given RSS url.
    The main class is RSSFeed which defines this logic.
    Item class handles the part of RSS xml -> <item> tags.
"""

### Import Necessary Modules and/or their contents ###
import re
import logging
import requests
from bs4 import BeautifulSoup
from constants import *
from exceptions import InvalidRSSException


class Item:
    """ Class which handles xml <item> tag. It is constructed by real <item> tag.
        Parses the tag and finds and stores the fields in itself.
    """
    def __init__(self, xml_item) -> None:
        """ The initializer of an Item object.
        """
        self.item = xml_item
        self.title = None
        self.link = None
        self.description = None
        self.extra_links = []
        self.date = None
        self.media = None
        self.set_fields()
        self.valid = self.is_valid()

    def set_fields(self):
        """ Method to call all the set() methods of an object
        """
        self.set_title()
        self.set_link()
        self.set_description()
        self.set_date()
        self.set_media()
    
    def is_valid(self) -> bool:
        """ Method that determines whether or not current item is valid.
            Remember, in order to be valid, an item must have at least: title, link, description, date.
            Returns the boolean representing the appropriate value.
        """
        if self.title and self.link and self.description and self.date:
            return True
        return False
    
    def set_title(self):
        """ Method to find and set the title of an item.
        """
        try:
            self.title = self.item.title.text
        except AttributeError:
            pass

    def set_link(self):
        """ Method to find and set the link of an item.
        """
        try:
            self.link = self.item.link.text
        except AttributeError:
            pass

    def set_description(self):
        """ Method to find and set the description of an item.
        """
        def clear_description(text: str) -> str:
            """ The helper function to clean the description if it contains some tags or special symbols.
            """
            new_text = re.sub(r"\<[^<>]*\>", " ", text)
            new_text = re.sub(r"\&[^&;]*\;", "-", new_text)
            if new_text.startswith("   "):
                new_text = new_text.replace("   ", "", 1)
            new_text = new_text.replace("    ", ". ")
            return new_text

        def find_links() -> list[str]:
            """ The helper function which finds all the links inside of item's description, which is in html format.
                Returns the list of string representation of these links.
            """
            links = []
            description_html = BeautifulSoup(self.item.description.text, 'html.parser')
            a_links = description_html.find_all('a')
            for link in a_links:
                links.append(link['href'])
            return links
        
        try:
            self.description = self.item.description.text
            if bool(BeautifulSoup(self.description, "html.parser").find()):
                self.extra_links = find_links()
            self.description = clear_description(self.description)
        except AttributeError:
            pass
    
    def set_date(self):
        """ Method to find and set the date of an item.
        """
        try:
            self.date = self.item.pubDate.text
        except AttributeError:
            pass
    
    def set_media(self):
        """ Method to find and set the image or other media of an item.
        """
        if self.item.enclosure:
            self.media = self.item.enclosure["url"]
        elif self.item.media:
            self.media = self.item.media["url"]
                   
            
class RSSFeed:
    """ Class which represents the rss feed of a particular (given by a user) url.
        It is initialized with a given global `RSS_URL` variable.
        It has an attribute `valid` to represent if a given url is a valid RSS url.
        If it is valid, `.parse_items()` can be called, otherwise, there's no logic to call that method.
    """
    def __init__(self) -> None:
        """ RSSFeed constructor
        """
        logging.info("Initializing an RSS feed...")
        try:
            self.soup = self.send_request()
            self.title = None
            self.set_title()
        except InvalidRSSException as exc:
            self.valid = False
            logging.error(exc.error_message)
        except TypeError:
            logging.error("Check out the providing url one more time!")
        else:
            self.valid = True
            logging.info("RSS Feed was set up successfully!")
    
    def send_request(self):
        """ Function which sends the request to an RSS_URL
            Raises exception in case of failure.
            Returns the BeautifulSoup object in case of success.
        """
        logging.info(f"Sending a request to '{RSS_URL}'...")
        response = requests.get(RSS_URL)
        logging.info("Response was taken successfully!")
        if response.status_code != 200:
            raise TypeError("Invalid url")
        soup = BeautifulSoup(response.content, "xml")
        return soup
    
    def set_title(self):
        """ Function which sets the title of a current RSS feed (if available)
        """
        channel = self.soup.find("channel")
        if channel:
            try:
                self.title = channel.title.text
            except AttributeError:
                pass
        else:
            raise InvalidRSSException
            
    def parse_items(self):
        """ Class method to parse the RSS <item>s in a given url.
            Returns the list of created Item objects which will have the required RSS fields.
        """
        logging.info("Starting to parse...")
        items = self.soup.find_all("item")
        items_limit = len(items) if LIMIT is None else LIMIT
        parsed_items = [] # the list of Item objects of `items` xml objects

        for i in range(items_limit):
            item = Item(items[i])
            parsed_items.append(item)
        
        logging.info("Parsing has finished!")
        
        return parsed_items
