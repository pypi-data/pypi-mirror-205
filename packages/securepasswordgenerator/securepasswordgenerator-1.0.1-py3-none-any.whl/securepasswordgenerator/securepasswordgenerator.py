#!/usr/bin/env python
"""
MIT License

Copyright (c) 2023-present Ali Fayaz (Quill) (quillfires)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import argparse
from random import SystemRandom
import string


def generate(length = 8,
             use_lower_case = True,
             use_upper_case = True,
             use_numbers = True,
             use_special = False,
             use_hex = False):
    """
    Normal Passwords - Default Passwords 8 characters with Upper case, Lower case and Numbers.
    """
    characters = ""
    saferand = SystemRandom()
    if use_lower_case:
        characters += string.ascii_lowercase
    if use_upper_case:
        characters += string.ascii_uppercase
    if use_numbers:
        characters += string.digits
    if use_special:
        characters += string.punctuation
    if use_hex:
        characters += "123456789ABCDEF"
    password = "".join(saferand.choice(characters) for i in range(length))
    return password


def decent():
    """
    Generate Memorable Passwords - Perfect for securing your computer or mobile device, or somewhere brute force is detectable.
    """
    password = generate(10, True, True, True, False, False)
    return password


def strong():
    """
    Generate Strong Passwords - Robust enough to keep your web hosting account secure.
    """
    password = generate(15, True, True, True, True, False)
    return password


def fort_knox():
    """
    Generate Fort Knox Passwords - Secure enough for almost anything, like root or administrator passwords.
    """
    password = generate(30, True, True, True, True, False)
    return password


def ci_key():
    """
    Generate CodeIgniter Encryption Keys - Can be used for any other 256-bit key requirement.
    """
    password = generate(32, True, True, True, False, False)
    return password


def wpa_160():
    """
    Generate 160-bit WPA Key
    """
    password = generate(20, True, True, True, True, False)
    return password


def wpa_504():
    """
    Generate 504-bit WPA Key
    """
    password = generate(63, True, True, True, True, False)
    return password


def wep_64():
    """
    Generate 64-bit WEP Keys
    """
    password = generate(5, False, False, False, False, True)
    return password


def wep_128():
    """
    Generate 128-bit WEP Keys
    """
    password = generate(13, False, False, False, False, True)
    return password


def wep_152():
    """
    Generate 152-bit WEP Keys
    """
    password = generate(16, False, False, False, False, True)
    return password


def wep_256():
    """
    Generate 256-bit WEP Keys
    """
    password = generate(29, False, False, False, False, True)
    return password


def main():
    parser = argparse.ArgumentParser(description="The Secure Password or Keygen Generator")
    parser.add_argument("length", nargs="?", default=8, action="store",
                        help="Length of password (default is 8 characters)")
    parser.add_argument("-l", "--lower-enable", dest="use_lower_case", default=True, action="store_true",
                        help="Use lowercase characters")
    parser.add_argument("-L", "--lower-disable", dest="use_lower_case", default=False, action="store_false",
                        help="Don't use lowercase characters")
    parser.add_argument("-u", "--upper-enable", dest="use_upper_case", default=True, action="store_true", 
                        help="use upper case characters")
    parser.add_argument("-U", "--upper-disable", dest="use_upper_case", default=False, action="store_false", 
                        help="don't use upper case characters")
    parser.add_argument("-n", "--number-enable", dest="use_numbers", default=True, action="store_true", 
                        help="use number characters")
    parser.add_argument("-N", "--number-disable", dest="use_numbers", default=False, action="store_false", 
                        help="don't use number characters")
    parser.add_argument("-s", "--special-enable", dest="use_special", default=False, action="store_true", 
                        help="use special characters")
    parser.add_argument("-S", "--special-disable", dest="use_special", default=True, action="store_false", 
                        help="don't use special characters")
    parser.add_argument("-x", "--hex-enable", dest="use_hex", default=False, action="store_true", 
                        help="use hex characters")
    parser.add_argument("-X", "--hex-disable", dest="use_hex", default=True, action="store_false", 
                        help="don't use hex characters")
    parser.add_argument("-DP", "--decent", dest="decent", default=False, action="store_true", 
                        help="Generate Memorable Passwords - Perfect for securing your computer or mobile device, or somewhere brute force is detectable.")
    parser.add_argument("-SP", "--strong", dest="strong", default=False, action="store_true", 
                        help="Generate Strong Passwords - Robust enough to keep your web hosting account secure.")
    parser.add_argument("-FP", "--fort_knox", dest="fort_knox", default=False, action="store_true", 
                        help="Generate Fort Knox Passwords - Secure enough for almost anything, like root or administrator passwords.")
    parser.add_argument("-ci", "--ci_key", dest="ci_key", default=False, action="store_true", 
                        help="Generate CodeIgniter Encryption Keys - Can be used for any other 256-bit key requirement.")
    parser.add_argument("-wpa160", "--wpa_160", dest="wpa_160", default=False, action="store_true", 
                        help="Generate 160-bit WPA Key")
    parser.add_argument("-wpa504", "--wpa_504", dest="wpa_504", default=False, action="store_true", 
                        help="Generate 504-bit WPA Key")
    parser.add_argument("-wep64", "--wep_64", dest="wep_64", default=False, action="store_true", 
                        help="Generate 64-bit WEP Keys")
    parser.add_argument("-wep128", "--wep_128", dest="wep_128", default=False, action="store_true", 
                        help="Generate 128-bit WEP Keys")
    parser.add_argument("-wep152", "--wep_152", dest="wep_152", default=False, action="store_true", 
                        help="Generate 152-bit WEP Keys")
    parser.add_argument("-wep256", "--wep_256", dest="wep_256", default=False, action="store_true", 
                        help="Generate 256-bit WEP Keys")
    args = parser.parse_args()
    
    if args.length is None:
        length = 8
    else:
        try:
            length = int(args.length)
        except ValueError:
            print(f"Error: Input length '{args.length}' is not a valid number")
            return
    
    if args.decent:
        password = decent()
        print(password)
        return
    
    if args.strong:
        password = strong()
        print(password)
        return
    
    if args.fort_knox:
        password = fort_knox()
        print(password)
        return
    
    if args.ci_key:
        password = ci_key()
        print(password)
        return
    
    if args.wpa_160:
        password = wpa_160()
        print(password)
        return
    
    if args.wpa_504:
        password = wpa_504()
        print(password)
        return
    
    if args.wep_64:
        password = wep_64()
        print(password)
        return
    
    if args.wep_128:
        password = wep_128()
        print(password)
        return
    
    if args.wep_152:
        password = wep_152()
        print(password)
        return
    
    if args.wep_256:
        password = wep_256()
        print(password)
        return
    
    if not args.use_lower_case and not args.use_upper_case and not args.use_numbers and not args.use_special and not args.hex:
        print("You have disabled all supported character sets. You must enable " + \
                "at least one of the character sets to generate a password.")
        return
    
    password = generate(length=length,
                        use_lower_case = args.use_lower_case,
                        use_upper_case = args.use_upper_case,
                        use_numbers = args.use_numbers,
                        use_special = args.use_special,
                        use_hex = args.use_hex)
    print(password)


if __name__ == "__main__":
    main()