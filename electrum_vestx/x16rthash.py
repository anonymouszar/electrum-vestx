# -*- coding: utf-8 -*-

import sys


try:
    from x16rt_hash import getPoWHash
    import_success = True
    load_libx16rthash = False
    errorMsg = 'Success'
except ImportError as error:
    import_success = False
    load_libx16rthash = True
    errorMsg = sys.exc_info()[0]


if load_libx16rthash:
    from ctypes import cdll, create_string_buffer, byref

    if sys.platform == 'darwin':
        name = 'libx16rthash.dylib'
    elif sys.platform in ('windows', 'win32'):
        name = 'libx16rthash-0.dll'
    else:
        name = 'libx16rthash.so'

    try:
        lx16rthash = cdll.LoadLibrary(name)
        x16rt_hash = lx16rthash.x16rt_hash
    except:
        load_libx16rthash = False


if load_libx16rthash:
    hash_out = create_string_buffer(32)

    def getPoWHash(header):
        x16rt_hash(header, byref(hash_out))
        return hash_out.raw


if not import_success and not load_libx16rthash:
    raise ImportError(errorMsg)
