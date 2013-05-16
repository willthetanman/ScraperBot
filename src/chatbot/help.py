# -*- coding: utf-8 -*-

"""
Help handler

"""


import dispatch

@dispatch.handler("help")
def help_handler(*args, **kwargs):
  return u"Comamnds Avaliable: " + \
  "\n" "@tanbot [ipv4, domain, md5hash]" \
  "\n" "@tanbot osint [ipv4, domain, md5hash]"

