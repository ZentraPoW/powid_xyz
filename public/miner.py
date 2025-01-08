
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

if len(sys.argv[1]) == 42:
    addr = sys.argv[1].lower()
    print('Address', addr)
    assert addr.startswith('0x')
    assert set(addr[2:]) <= set('abcdef0123456789')
    handle = addr
else:
    HANDLE_LETTERS = 'abcdefghijklmnopqrstuvwxyz0123456789_'
    handle = sys.argv[1]
    print('POWid', handle)
    assert len(handle) > 4 and len(handle) < 42
    assert set(handle) <= set(HANDLE_LETTERS)
    addr = None

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

        if addr:
            req = requests.get('%s/get_lottery' % (HOST,))
        else:
            req = requests.get('%s/get_lottery?handle=%s' % (HOST, handle))
        lottery = req.json()
        addr2 = lottery.get('addr', addr)
        # print(addr2, addr)
        # assert addr2.startswith('0x')

        # header = binascii.unhexlify('0000c0206373edd370dd69a39a72b54efa77cf1f9a371ca74dea02000000000000000000688c15b309e94ce0eea1c486336e10fcf0dc8f208a4ed1874dd0723023f5f9a2ad461366d362031732862496')
        # nonce = 0x96248631
        while nonce <= 0xffffffff:
            header = header[0:76] + nonce.to_bytes(4, byteorder='little')
            # h = hashlib.sha256(hashlib.sha256(header).digest()).digest()[::-1]
            h = hashlib.sha256(hashlib.sha256(header).digest()).digest()
            h_int = uint256_from_str(h)

            if lottery['available']:
                p = hashlib.sha256(h+binascii.unhexlify(addr2[2:])).digest()
                p_int = int.from_bytes(p, 'big')
                for amount in sorted([int(i) for i in lottery['difficulties'].keys()], reverse=True):
                    f_int = lottery['difficulties'][str(amount)]
                    if p_int < f_int:
                        print(datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S'), 'Meet redeem difficulty', header.hex(), amount)
                        req = requests.post('%s/redeem_lottery?preimage=%s&addr=%s&amount=%s' % (HOST, header.hex(), addr2, amount))
                        break

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
        seconds_waiting = 2

    except:
        time.sleep(seconds_waiting)
        print(datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S'), 'Retry after %s seconds' % seconds_waiting)
        seconds_waiting *= 2
