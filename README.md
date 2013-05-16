ScraperBot
======

ScraperBot is a Skype chat bot that preforms OSINT on a given IP, Domain or Hash

## Main Dependencies:
- Skype4Py

## Handler Dependencies:
- sudo easy_install Skype4Py
- sudo easy_install SQLAlchemy
- sudo easy_install argparse
- sudo easy_install httplib2
- sudo easy_install whoosh
- sudo easy_install pattern

## How to run:

1. Install dependencies
2. Launch Skype
3. cd into the directory hosting chatbot
4. run the chatbot with: python chatbot.py
5. The skypebot automatically assumes your name, refer to usage below for interaction

## Usage:
- @[skype_handle] [ipv4, domain, md5hash]
- @[skype_handle] osint [ipv4, domain, md5hash]
