""" A script that contains all the tests written for this program.
    It mainly tests `url_parse` module since it implements the main logic of a program.
"""

### Import necessary modules and/or functions ###
import unittest
from unittest.mock import patch
from bs4 import BeautifulSoup
from url_parse import Item, RSSFeed


class TestItem(unittest.TestCase):
    """ The test Class that contains all tests written for testing Item class.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """ The classmethod that sets up an item needed to construct Item object for testing purposes.
        """
        string_item = "<item><title>На набережной вновь чистота и порядок [ВИДЕО]</title><description>\
            К началу недели на Онежской набережной ни соринки.</description><link>https://vse.sale/news/view/37518\
            </link><guid>https://vse.sale/news/view/37518</guid><pubDate>Mon, 27 Jun 2022 15:34:00 +0300</pubDate>\
            <enclosure url=\"http://vse.sale/files/news/2022/06/102375_1656333354.jpg\" length=\"44857\" type=\"image/jpeg\"/>\
            </item>"
        cls.soup_item = BeautifulSoup(string_item, "xml")
        cls.item = Item(cls.soup_item)
    
    def test_fields(self):
        """ Test the fields of a created item, as well as the validity of an item.
        """
        self.assertTrue(self.item.title is not None)
        self.assertTrue(self.item.link is not None)
        self.assertTrue(self.item.description is not None)
        self.assertTrue(self.item.media is not None)
        self.assertTrue(self.item.date is not None)
        self.assertTrue(self.item.valid)
    
    def test_is_valid(self):
        """ Test `.is_valid()` method of an `Item` in different conditions.
        """
        temp = self.item.title
        self.item.title = None
        self.assertFalse(self.item.is_valid())
        self.item.title = temp
        self.assertTrue(self.item.is_valid())
        self.item.media = None
        self.assertTrue(self.item.is_valid())
    
    def test_set_fields(self):
        """ Test `.set_fields` method of an Item with a help of `test_fields` test.
        """
        self.item.title = None
        self.item.link = None
        self.item.description = None
        self.item.date = None
        self.item.media = None
        self.item.set_fields()
        self.test_fields()
    
    def test_set_media(self):
        """ Test `.set_media` method of an Item
        """
        removing_field = self.item.media
        self.item.media = None
        self.item.set_media()
        self.assertTrue(self.item.media is not None)
        self.assertEqual(self.item.media, removing_field)
    
    def test_set_date(self):
        """ Test `.set_date` method of an Item
        """
        removing_field = self.item.date
        self.item.date = None
        self.item.set_date()
        self.assertTrue(self.item.date is not None)
        self.assertEqual(self.item.date, removing_field)
    
    def test_set_link(self):
        """ Test `.set_link` method of an Item
        """
        removing_field = self.item.link
        self.item.link = None
        self.item.set_link()
        self.assertTrue(self.item.link is not None)
        self.assertEqual(self.item.link, removing_field)
    
    def test_set_title(self):
        """ Test `.set_title` method of an Item
        """
        removing_field = self.item.title
        self.item.title = None
        self.item.set_title()
        self.assertTrue(self.item.title is not None)
        self.assertEqual(self.item.title, removing_field)
    
    def test_set_description(self):
        """ Test `.set_description` method of an Item in two different types of possible desciptions
        """
        removing_field = self.item.description
        self.item.description = None
        self.item.set_description()
        self.assertTrue(self.item.description is not None)
        self.assertEqual(self.item.description, removing_field)

        self.item.description = '<ol><li><a href="https://news.google.com/__i/rss/rd/articles/\
            CBMibWh0dHBzOi8vd3d3LmNic25ld3MuY29tL2xpdmUtdXBkYXRlcy9zdXByZW1lLWNvdXJ0LWpvZS1rZW5uZWR5LWhpZ2gtc2Nob29sLWZvb3RiYWxsL\
            WNvYWNoLXNjaG9vbC1wcmF5ZXItY2FzZS_SAXFodHRwczovL3d3dy5jYnNuZXdzLmNvbS9hbXAvbGl2ZS11cGRhdGVzL3N1cHJlbWUtY291cnQtam9lLW\
            tlbm5lZHktaGlnaC1zY2hvb2wtZm9vdGJhbGwtY29hY2gtc2Nob29sLXByYXllci1jYXNlLw?oc=5" target="_blank">Supreme Court sides\
            with high school football coach who lost his job for praying after games</a>&nbsp;&nbsp;<font color="#6f6f6f">CBS News</font></li><li><a href="https://news.google.com/__i/rss/rd/articles/\
            CBMiaWh0dHBzOi8vd3d3LmZveG5ld3MuY29tL3BvbGl0aWNzL2hpZ2gtc2Nob29sLWZvb3RiYWxsLWNvYWNoLXNjb3Jlcy1iaWctd2luLXN1cHJlbWUtY\
            291cnQtcG9zdC1nYW1lLXByYXllctIBbWh0dHBzOi8vd3d3LmZveG5ld3MuY29tL3BvbGl0aWNzL2hpZ2gtc2Nob29sLWZvb3RiYWxsLWNvYWNoLXNjb3Jlcy1iaWctd2luLXN1cHJlbWUtY291cnQtcG9zdC1nYW1lLXByYXllci5hbXA?oc=5" target="_blank">High school football coach scores\
            big win at Supreme Court over post-game prayer</a>&nbsp;&nbsp;<font color="#6f6f6f">Fox News</font></li><li><a\
            href="https://news.google.com/__i/rss/rd/articles/\
            CBMiamh0dHBzOi8vd3d3LmNubi5jb20vMjAyMi8wNi8yNy9wb2xpdGljcy9mb290YmFsbC1jb2FjaC1wcmF5ZXItaGlnaC1zY2hvb2wtc3VwcmVtZS1jb\
            3VydC1rZW5uZWR5L2luZGV4Lmh0bWzSAW5odHRwczovL2FtcC5jbm4uY29tL2Nubi8yMDIyLzA2LzI3L3BvbGl0aWNzL2Zvb3RiYWxsLWNvYWNoLXByYXllci1oaWdoLXNjaG9vbC1zdXByZW1lLWNvdXJ0LWtlbm5lZHkvaW5kZXguaHRtbA?oc=5" target="_blank">Supreme Court further erodes\
            separation between church and state in case of praying football coach</a>&nbsp;&nbsp;<font color="#6f6f6f">CNN</font></li><li><a href="https://news.google.com/__i/rss/rd/articles/\
            CBMidGh0dHBzOi8vd3d3LmJsb29tYmVyZy5jb20vb3Bpbmlvbi9hcnRpY2xlcy8yMDIyLTA2LTI3L3N1cHJlbWUtY291cnQtdXBlbmRzLWNodXJjaC1zd\
            GF0ZS1sYXctaW4tY2FzZS1vZi1wcmF5aW5nLWNvYWNo0gEA?oc=5" target="_blank">Supreme Court Upends Church-State Law in Case\
            of Praying Coach</a>&nbsp;&nbsp;<font color="#6f6f6f">Bloomberg</font></li></ol>'
        self.item.set_description()
        self.assertTrue(self.item.extra_links is not None)


class TestRSSFeed(unittest.TestCase):
    """ Class to implement test functions/methods for checking RSSFeed functionality
    """

    @classmethod
    @patch("url_parse.RSS_URL", "https://vse.sale/news/rss")
    def setUpClass(cls) -> None:
        """ Set up the RSSFeed object for using while testing.
        """
        cls.rss_feed = RSSFeed()
    
    def test_constructor(self):
        """ Test the initializer `__init__()` method of as `RSSFeed`
        """
        self.assertTrue(self.rss_feed.title is not None)
        self.assertTrue(self.rss_feed.valid)
    
    @patch("url_parse.RSS_URL", "https://vse.sale/news/rss")
    def test_send_request(self):
        """ Test `.send_request()` method of an `RSSFeed` class
        """
        self.assertTrue(isinstance(self.rss_feed.send_request(), BeautifulSoup))
    
    @patch("url_parse.LIMIT", 5)
    def test_parse_items(self):
        """ Test `.parse_items()` method of an `RSSFeed` class
        """
        items = self.rss_feed.parse_items()
        self.assertTrue(isinstance(items, list))
        self.assertTrue(isinstance(items[0], Item))
        self.assertEqual(len(items), 5)
    
    def test_set_title(self):
        """ Test `.set_title` method of an RSSFeed class
        """
        self.rss_feed.title = None
        self.assertTrue(self.rss_feed.title is None)
        self.rss_feed.set_title()
        self.assertTrue(self.rss_feed.title is not None)


if __name__ == "__main__":
    unittest.main()