import base64
import re
import struct

r = re.compile(r'=+$')

def encode(value):
    if value <= 0xFF:
        s = struct.pack('<B', value)
    elif value > 0xFF and value <= 0xFFFF:
        s = struct.pack('<H', value)
    elif value > 0xFFFF:
        s = struct.pack('<I', value)
    s = base64.urlsafe_b64encode(s)
    return r.sub('', s)

def decode(s):
    original_s = s
    s += (len(s) % 4) * '='
    s = base64.urlsafe_b64decode(s)
    if len(original_s) <= 2:
        value = struct.unpack('<B', s)
    elif len(original_s) > 2 and len(original_s) <= 4:
        value = struct.unpack('<H', s)
    elif len(original_s) > 4:
        value = struct.unpack('<I', s)

    return value

if __name__ == '__main__':
    for i in range(65534,65600):
        e = encode(i)
        print "e = ", e
        print "d = ", decode(e)
