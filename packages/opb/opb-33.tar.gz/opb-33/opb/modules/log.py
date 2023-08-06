# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,R0903,E0402


'log'


import time


from ..clocked import elapsed
from ..persist import Class, find, fntime, write
from ..objects import Object


def __dir__():
    return (
            'Log',
            'log',
           )


class Log(Object):

    def __init__(self):
        super().__init__()
        self.txt = ''


Class.add(Log)


def log(event):
    if not event.rest:
        nmr = 0
        for obj in find('log'):
            event.reply('%s %s %s' % (
                                      nmr,
                                      obj.txt,
                                      elapsed(time.time() - fntime(obj.__oid__)))
                                     )
            nmr += 1
        if not nmr:
            event.reply('no log')
        return
    obj = Log()
    obj.txt = event.rest
    write(obj)
    event.reply('ok')
