# -*- coding: utf-8 -*-

"""
Help handler

"""


import dispatch

@dispatch.handler("help")
def help_handler(*args, **kwargs):
  return u"Comamnds Avaliable: " \
  "\n" "Aliases: @tanbot800, @tanbot, @tbot, @osint" \
  "\n" "@alias [ipv4, domain, md5hash]" \
  "\n" "@alias osint [ipv4, domain, md5hash]" \
  "\n" \
  "\n" "Examples:" \
  "\n" "@osint 192.168.1.1" \
  "\n" "@osint google[.]com" \
  "\n" "@osint 02d6519b0330a34b72290845e7ed16ab"
