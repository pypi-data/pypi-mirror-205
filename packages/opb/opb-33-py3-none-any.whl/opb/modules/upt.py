# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,E0402


"uptime"


import time


from ..clocked import elapsed


def __dir__():
    return (
            'upt',
           )


__all__ = __dir__()


starttime = time.time()


def upt(event):
    event.reply(elapsed(time.time()-starttime))
