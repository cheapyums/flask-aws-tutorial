#-------------------------------------------------------------------------------
# Name:        coupon_encoder
# Purpose:     encode a coupon ID meeting the following requirements:
#              1) ease to read over the phone (avoid lookalike chars like
#                 I/L/O that can be confused with 0/1)
#              2) hard to guess
#              3) less likely to generate f* words
#
# Author:      Paulo Scardine <paulos at xtend.com.br>
#
# Created:     17/09/2012
# Copyright:   (c) Paulo Scardine 2012
# Licence:     BSD
#-------------------------------------------------------------------------------
#!/usr/bin/env python
"""
The purpose of this enconding scheme is generating coupon codes.
It can encode/decode a positive integer in a base 32 scheme where:
  - to make it easy to read over the phone, chars I/L/O are not used
    (avoids confusion with 1/0)
  - char U is not used (to decrease the possibility of f* words)
  - the generated codes are not trivial to guess
"""

import random

DIGITS = 'ABCDEFGHJKMNPQRSTWVXYZ0123456789'
TRANSLATE = { 'O': '0', 'I': '1', 'L': '1' }

class InvalidKeyException(Exception):
    pass

class InvalidCodeException(Exception):
    pass

class CouponEncoder(object):
    """CouponEncoder()
    Initialize this object with a key made with the characters
    'ABCDEFGHJKMNPQRSTWVXYZ0123456789' in random order.
    Example:
        >>> c = CouponEncoder('10BEH8G426RADWZVF9JPKX5QMC3YTN7S')
        >>> c.encode(15171013)
        'FS19E'
        >>> c.decode('FS19E')
        15171013
        >>> code, check = c.encode_with_verification(1234)
        ('NH4RZ', '782AV')
        >>> c.is_valid(code, check)
        True
        >>> c.is_valid(code, '782AA')
        False
    """
    def __init__(self, key):
        self.key = key.upper()
        msg = 'key should be the sequence {0} in random order'.format(DIGITS)
        if len(set(self.key)) != 32:
            raise InvalidKeyException(msg)
        for c in key:
            if c not in DIGITS:
                raise InvalidKeyException(msg)
    def v_key(self, key):
        return self.key[(self.key.index(key) + 1) % 32]
    def encode(self, number, key='A', num_digits=5):
        """Encodes a positive integer into suitable coupon code"""
        number = int(number)
        if number < 0:
            raise ValueError('number should be a positive integer')
        if number > self.max_value(num_digits):
            msg = "Can't encode {0} with {1} digits"
            raise OverflowError(msg.format(number, num_digits))
        format_str = '{{0:0{0:d}b}}'.format(num_digits*5)
        bits = format_str.format(number)
        chunks = [ bits[i:i+5] for i in range(0, len(bits), 5) ]
        code = ''
        for i, chunk in enumerate(reversed(chunks)):
            key = self.key[(i + int(chunk, 2) + self.key.index(key)) % 32]
            code += key
        return code
    def max_value(self, num_digits=5):
        """Returns the maximum value that can be encoded with the
        given number of digits"""
        return 32 ** num_digits - 1
    def encode_with_verification(self, number, key='A', l=5):
        """Returns a tuple containing a coupon code and a verification code"""
        v_key = self.v_key(key)
        return self.encode(number, key, l), self.encode(number, v_key, l)
    def decode(self, code, key='A'):
        """Decodes a coupon code into the original positive integer"""
        code = code.upper()
        for digit in code:
            if digit not in DIGITS and digit not in TRANSLATE:
                msg = 'Invalid digit "{0}" in code'
                raise InvalidCodeException(msg.format(digit))
        bits = ''
        for i, digit in enumerate(code):
            if digit in TRANSLATE:
                digit = TRANSLATE[digit]
            d = self.key.index(digit) - self.key.index(key) - i
            while d < 0: d += 32
            key = digit
            bits = '{0:05b}{1}'.format(d, bits)
        return int(bits, 2)
    def is_valid(self, code, verification_code, key='A'):
        """Checks if a code is valid given a code and a verification code"""
        v_key = self.v_key(key)
        return self.decode(code, key) == self.decode(verification_code, v_key)

def main():
    digits = [ d for d in DIGITS]
    random.shuffle(digits)
    print __doc__
    print CouponEncoder.__doc__
    print "Suggested key:", ''.join(digits)

if __name__ == '__main__':
    main()

