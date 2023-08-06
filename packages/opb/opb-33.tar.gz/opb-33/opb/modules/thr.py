# This file is placed in the Public Domain.
# pylint: disable=C0114,C0115,C0116,E1101,E0402


"list running threads."


import threading
import time


from ..clocked import elapsed
from ..objects import Object, update


def __dir__():
    return (
            'thr',
           )


__all__ = __dir__()


starttime = time.time()


def thr(event):
    result = []
    for thread in sorted(threading.enumerate(), key=lambda x: x.getName()):
        if str(thread).startswith('<_'):
            continue
        obj = Object()
        update(obj, vars(thread))
        if getattr(obj, 'sleep', None):
            uptime = obj.sleep - int(time.time() - obj.state.latest)
        elif getattr(obj, 'starttime', None):
            uptime = int(time.time() - obj.starttime)
        else:
            uptime = int(time.time() - starttime)
        result.append((uptime, thread.name))
    res = []
    for uptime, txt in sorted(result, key=lambda x: x[0]):
        res.append('%s/%s' % (txt, elapsed(uptime)))
    if res:
        event.reply(' '.join(res))
    else:
        event.reply('no threads')
