# -*- coding: utf-8 -*-

"""
Chatbot CLI

"""

import os
import sys

# Bootstrap some externals
sys.path.insert(0, os.path.abspath("src"))
# sys.path.insert(0, os.path.abspath("src/py2"))
sys.path.insert(0, os.path.abspath("ext/sqlalchemy/lib"))
sys.path.insert(0, os.path.abspath("ext/whoosh/src"))
# sys.path.insert(0, os.path.abspath("ext/yelp-python-client"))


import chatbot

def main():
    bot = chatbot.Bot()
    bot.connect_and_listen()

if __name__ == "__main__":
	main()