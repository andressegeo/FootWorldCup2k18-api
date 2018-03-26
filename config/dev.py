"""
This file containg the dev config of the application.
"""
import logging

CONFIG_dev = {  
    u"db": {
        u"user": u"root",
        u"host" : u"127.0.0.1",
        u"password": u"namesgeo",
        u"database": u"FootWorldCup2k18",
        u"charset": u"utf-8"
    },
    u"logging": {
        u"level": logging.INFO,
        u"pattern": u'%(message)s',
        u"pattern_debug": u'[%(levelname)8s]-[%(asctime)16s]-[%(msecs)4d ms]-[%(filename)15s::%(funcName)15s]-[l.%(lineno)3s] %(message)s'
    }
}