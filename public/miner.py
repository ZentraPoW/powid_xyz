
import sys
import hashlib
import binascii
import struct
import datetime

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
while True:
    req = requests.get('%s/get_work?handle=%s' % (HOST, handle))
    header_hex = req.text
    print(datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S'), 'Header', header_hex)

    nonce = 0
    header = binascii.unhexlify(header_hex)
    # d_int = diff1 // difficulty
    d_cur = 0x00000f00ffff0000000000000000000000000000000000000000000000000000

    # header = binascii.unhexlify('0000c0206373edd370dd69a39a72b54efa77cf1f9a371ca74dea02000000000000000000688c15b309e94ce0eea1c486336e10fcf0dc8f208a4ed1874dd0723023f5f9a2ad461366d362031732862496')
    # nonce = 0x96248631
    while nonce <= 0xffffffff:
        header = header[0:76] + nonce.to_bytes(4, byteorder='little')
        # h = hashlib.sha256(hashlib.sha256(header).digest()).digest()[::-1]
        h = hashlib.sha256(hashlib.sha256(header).digest()).digest()
        h_int = uint256_from_str(h)
        # print(h_int)
        # print(d_int, h_int < d_int)
        # if h_int < d_int:
        #     print('result', h[::-1].hex(), nonce)
        #     break
        if h_int < d_cur:
            d_cur = h_int
            # print(h[::-1].hex())
            # print(h_int, nonce)
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
                # print(req.text)
                break
        nonce += 1
