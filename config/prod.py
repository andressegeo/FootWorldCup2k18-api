"""
This file containg the prod config of the application.
"""
import logging

CONFIG_prod = {
    u"db": {
        u"unix_socket": u"",
        u"user": u"root",
        u"host" : u"",
        u"password": u"",
        u"database": u"",
        u"charset": u""
    },
    u"logging": {
        u"level": logging.INFO,
        u"pattern": u'%(message)s',
        u"pattern_debug": u'[%(levelname)8s]-[%(asctime)16s]-[%(msecs)4d ms]-[%(filename)15s::%(funcName)15s]-[l.%(lineno)3s] %(message)s'
    }
}