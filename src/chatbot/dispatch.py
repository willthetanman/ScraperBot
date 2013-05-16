# -*- coding: utf-8 -*-

"""
Dispatch: dispatch commands to command handlers

"""


__all__ = ["HANDLERS", "register_handler", "dispatch_to_handlers"]


HANDLERS = {}


def handler(command, prepend=False):
    def decorator(f):
        register_handler(command, f, prepend=prepend)
        def wrapper(*args, **kwargs):
            return f.__call__(*args, **kwargs)
        return wrapper
    return decorator


def register_handler(command, handler, prepend=False):
    global HANDLERS
    if command in HANDLERS and handler not in HANDLERS[command]:
        if prepend:
            HANDLERS[command].insert(0, handler)
        else:
            HANDLERS[command].append(handler)
    else:
        HANDLERS[command] = [handler]


def dispatch_to_handlers(command, *args, **kwargs):
    global HANDLERS
    if command not in HANDLERS:
        return
    
    # loop through and execute all handlers. keep going until a handler returns a string.
    # if a handler throws an exception or returns False, keep going
    for handler in HANDLERS[command]:
        try:
            result = handler(*args, **kwargs)
            if result is False:
                continue
            return result
        except Exception, e:
            print "Error in handler", handler
            import traceback
            traceback.print_exc()

