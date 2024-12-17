
import sys
import hashlib
import binascii
import struct
import datetime
import time

import requests


def uint256_from_str(s):
    r = 0
    t = struct.unpack("<IIIIIIII", s[:32])
    for i in range(8):
        r += t[i] << (i * 32)
    return r

diff1 = 0x00000000ffff0000000000000000000000000000000000000000000000000000

HANDLE_LETTERS = 'abcdefghijklmnopqrstuvwxyz0123456789_'

handle = sys.argv[1]
print('POWid', handle)
assert len(handle) > 4 and len(handle) < 42
assert set(handle) <= set(HANDLE_LETTERS)

HOST = 'https://submit.powid.xyz'
seconds_waiting = 2
while True:
    try:
        req = requests.get('%s/get_work?handle=%s' % (HOST, handle))
        header_hex = req.text
        print(datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S'), 'Header', header_hex)

        nonce = 0
        header = binascii.unhexlify(header_hex)
        d_cur = 0x00000f00ffff0000000000000000000000000000000000000000000000000000

        while nonce <= 0xffffffff:
            header = header[0:76] + nonce.to_bytes(4, byteorder='little')
            h = hashlib.sha256(hashlib.sha256(header).digest()).digest()
            h_int = uint256_from_str(h)

            if h_int < d_cur:
                d_cur = h_int
                req = requests.post('%s/submit_work?handle=%s&nonce=%s' % (HOST, handle, nonce))
                print(datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S'), 'Submit PoW', nonce)
                if req.text != header_hex:
                    print('New Block')
                    print(req.text)
                    break

            if nonce % 10000000 == 0 and nonce > 0:
                req = requests.get('%s/get_work?handle=%s' % (HOST, handle))
                print(datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S'), 'Checking New', nonce)
                if req.text != header_hex:
                    print(datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S'), 'New Block')
                    break
            nonce += 1

    except:
        time.sleep(seconds_waiting)
        print(datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S'), 'Retry after %s seconds' % seconds_waiting)
        seconds_waiting *= 2
