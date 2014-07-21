import sys
import logging
import argparse

from twisted.internet import reactor
from twisted.python import log
from twisted.web import server, resource


DESCRIPTION = """
A simulator for mlab-ns which is augmented with new features to support Ooni integration.
"""

PORT = 8585


def main(args=sys.argv[1:], _reactor=reactor):
    opts = parse_args(args)
    init_logging(getattr(logging, opts.loglevel))

    root = resource.Resource()
    site = server.Site(root)
    _reactor.listenTCP(PORT, site)

    _reactor.run()


def parse_args(args):
    p = argparse.ArgumentParser(
        description=DESCRIPTION,
        formatter_class=argparse.RawTextHelpFormatter)

    p.add_argument('--log-level',
                   dest='loglevel',
                   default='DEBUG',
                   choices=['DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL'],
                   help='Set logging level.')

    return p.parse_args(args)



LogFormat = '%(asctime)s %(levelname) 5s %(name)s | %(message)s'
DateFormat = '%Y-%m-%dT%H:%M:%S%z'

def init_logging(level):
    logging.basicConfig(
        stream=sys.stdout,
        format=LogFormat,
        datefmt=DateFormat,
        level=level)

    log.PythonLoggingObserver().start()


