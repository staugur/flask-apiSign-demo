# -*- coding: utf-8 -*-
"""
    utils.tool
    ~~~~~~~~~~~~~~

    Common function.

    :copyright: (c) 2017 by taochengwei.
    :license: MIT, see LICENSE for more details.
"""

import hashlib, time, datetime

md5 = lambda pwd: hashlib.md5(pwd).hexdigest()
get_current_timestamp = lambda: int(time.mktime(datetime.datetime.now().timetuple()))
