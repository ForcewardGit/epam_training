""" Module that handles the logic of parsing command line arguments.
    It defines the important function of performing this logic. It is used in main.py file
"""

### Importing necessary modules and/or their content ###
from argparse import ArgumentParser
import constants

def parse_arguments():
    """ Function to parse the provided arguments to a main program 
        and set up the variables from `constants.py` appropriately.
    """
    ### Create and initialize a parser ###
    arg_parser = ArgumentParser(
        prog = "RSS Parser",
        description = "Enter the url of RSS feed"
    )

    ### Handle the arguments of a parser ###
    arg_parser.add_argument(
        "--version",
        action = "store_true",
        help = "get the version info of a program"
    )
    arg_parser.add_argument(
        "--json",
        action = "store_true",
        help = "get the json representation as output"
    )
    arg_parser.add_argument(
        "--verbose",
        action = "store_true",
        help = "increase the output message verbosity"
    )
    arg_parser.add_argument(
        "--limit",
        help = "limit the number of feeds in output",
        type = int,
    )
    arg_parser.add_argument(
        "source",
        help = "The RSS url source.",
        nargs = "?"
    )

    ### Parse the arguments ###
    args = arg_parser.parse_args()

    ### Modify constants ###
    constants.RSS_URL = args.source
    if args.version:
        constants.VERSION_FLAG = True
    if args.json:
        constants.JSON_FLAG = True
    if args.verbose:
        constants.DEBUG_MODE = True
    if args.limit is not None and args.limit > 0:
        constants.LIMIT = args.limit
