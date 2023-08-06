# This file is placed in the Public Domain.
# pylint: disable=E0402


"runtime"


import os
import time


from .objects import Default


Cfg = Default()
Cfg.debug = False
Cfg.mod = ",cmd,err,irc,log,rss,sts,tdo,thr"
Cfg.name = "opb"
Cfg.skip = "PING,PONG"
Cfg.verbose = False
Cfg.workdir = os.path.expanduser("~/%s" % Cfg.name)


date = time.ctime(time.time()).replace('  ', ' ')
