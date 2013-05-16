tanbot
======

Tanbot is a Skype chat bot that preforms OSINT on a given IP, Domain or Hash

## Main Dependencies:
- Skype4Py

## Handler Dependencies:
- SQLAlchemy (for logging and url handler)
- Argparse (for message parsing)
- Httplib2 (For Yelp Lunch Handler)
- Whoosh (for searching)
- Pattern (for web searching)

## How to run:

1. Install dependencies
2. Launch Skype
3. cd into the directory hosting chatbot
4. run the chatbot with: python chatbot.py
5. The skypebot automatically assumes your name, so have somebody send you a message like:   [your name] hello

## Usage:
@tanbot [ipv4, domain, md5hash]
@tanbot osint [ipv4, domain, md5hash]
