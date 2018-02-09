# -*- coding: utf-8 -*-
# Created: 04.02.18
# Changed: 04.02.18

import logging
import datetime


def _log(func):
    """ Setup logging decorate function """

    def wrapper(message):

        LOG_FORMAT = "%(levelname)s %(asctime)s :: %(message)s"
        logging.basicConfig(filename="error.log",
                            level=logging.DEBUG,
                            format=LOG_FORMAT)
        logger = logging.getLogger()
        logger.error(message)
        return func(message)

    return wrapper
