	# -*- coding: utf-8 -*-

"""
Help handler

"""


import dispatch

@dispatch.handler("help")
def help_handler(*args, **kwargs):
  return u"Comamnds Avaliable: " + \
  "\n" "@" + chatbotself.get_name() + " [ipv4, domain, md5hash]" \
  "\n" "@" + chatbotself.get_name() + " osint [ipv4, domain, md5hash]"