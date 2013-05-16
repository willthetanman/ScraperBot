# -*- coding: utf-8 -*-

"""
Message parsing

"""

import codecs
import re
import shlex

__all__ = ["parse_command", "parse_message","parse_command_as_arg"]


URL_REGEX_STRING = r"(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?]))"
URL_REGEX = re.compile(URL_REGEX_STRING, re.U)

TAG_REGEX_STRING = r"(?:^|\s)[#]([\w-]+)"
TAG_REGEX = re.compile(TAG_REGEX_STRING, re.U)


def parse_command(content):
    # split into command and arguments
    
    try:
        byte_content = codecs.encode(content, 'utf-8')
        byte_tokens = shlex.split(byte_content, False, False)
        tokens = [codecs.decode(token, 'utf-8', 'replace') for token in byte_tokens]
    except Exception, e:
        tokens = content.split(' ')

    return (tokens[0], tokens[1:])


def parse_message(content):
    # parse message for urls and tags
    urls = [match[0] for match in URL_REGEX.findall(content)]
    
    tags = [match for match in TAG_REGEX.findall(content)]
    return (tags, urls)

def parse_command_check(content):

    content = str(content)
    rpd7 = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', re.IGNORECASE)
    rpdFind7 = re.findall(rpd7,content)
    rpdSorted7=sorted(rpdFind7)
    rpdSorted7=str(rpdSorted7)
    rpdSorted7=rpdSorted7[2:-2]

    rpd8 = re.compile('(.+\.)?([^.]+)\.\w{2,6}$', re.IGNORECASE)
    rpdFind8 = re.findall(rpd8,content)
    rpdSorted8=sorted(rpdFind8)
    rpdSorted8=str(rpdSorted8)
    rpdSorted8=rpdSorted8[2:-2]

    rpd9 = re.compile('[a-fA-F0-9]{32}', re.IGNORECASE)
    rpdFind9 = re.findall(rpd9,content)
    rpdSorted9=sorted(rpdFind9)
    rpdSorted9=str(rpdSorted9)
    rpdSorted9=rpdSorted9[2:-2]

    if rpdSorted7 == content:
        # print '--------------------------------'
        # print 'Parse Check: ' + content + ' is an IP. '
        return True

    elif rpdSorted9 == content:
        # print '--------------------------------'
        # print 'Parse Check: ' + content + ' is an MD5 Hash. '
        return True

    elif rpdSorted8 == content:
        # print '--------------------------------'
        # print 'Parse Check: ' + content + ' is a URL.  '
        return True

    else:
        return False
