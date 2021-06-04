import logging
from logging import StreamHandler, Formatter, getLogger

def getlog():
    """
    returns configured logger

    Usage:
        from defaultlog import log
    """
    fmt = Formatter(fmt='[%(name)s:%(levelname)s]:%(message)s (%(filename)s:%(lineno)s, time=%(asctime)s)',
                    datefmt='%b-%d %H:%M')

    # stream
    stream = StreamHandler()
    stream.setFormatter(fmt)

    # silence noisy packages
    for x in ["gensim", "pika"]:
        getLogger(x).setLevel(logging.WARNING)

    # root logger
    log = getLogger()
    log.handlers = [stream]
    log.setLevel(logging.INFO)
    return log

log = getlog()