import math
def encode_7_segment_display(text):

    encoding = {
        '0': '1111110',
        '1': '0110000',
        '2': '1101101',
        '3': '1111001',
        '4': '0110011',
        '5': '1011011',
        '6': '1011111',
        '7': '1110000',
        '8': '1111111',
        '9': '1111011',
        'A': '1110111',
        'B': '0011111',
        'C': '1001110',
        'D': '0111101',
        'E': '1001111',
        'F': '1000111',
        'G': '1011110',
        'H': '0110111',
        'I': '0110000',
        'J': '0111100',
        'K': '0110111',
        'L': '0001110',
        'M': '0010101',
        'N': '0010101',
        'O': '1111110',
        'P': '1100111',
        'Q': '1110011',
        'R': '0000101',
        'S': '1011011',
        'T': '0001111',
        'U': '0111110',
        'V': '0111110',
        'W': '0011111',
        'X': '0110111',
        'Y': '0111011',
        'Z': '1101101',
        ' ': '0000000',
        '.': '0100000',
        '-': '0000100',
        '_': '0000010',
        ',': '0100000',
        '!': '0100010',
        '?': '1110010',
        '\'': '0100000',
        '/': '0000000',
        '(': '0011100',
        ')': '0000111',
        '[': '1001110',
        ']': '1111000',
        '{': '1001110',
        '}': '1111000',
        '<': '0110000',
        '>': '0000101',
        '%': '0100101',
        '+': '0000110',
        '=': '0000101',
        ':': '0000101',
        ';': '0100100',
        '*': '0000000',
        '#': '0101010',
        '$': '0101011',
        '&': '0000000',
        '@': '0101110',
    }
    encoded = ""
    for c in text.upper():
        if c in encoding:
            encoded += encoding[c]
    return encoded

def encode_ascii85(text):

    padding = (4 - (len(text) % 4)) % 4
    text += "\0" * padding
    encoded = "<~"
    for i in range(0, len(text), 4):
        block = text[i:i+4]
        num = 0
        for c in block:
            num = num * 256 + ord(c)
        if num == 0:
            encoded += "z"
        else:
            enc_block = ""
            for j in range(5):
                enc_block = chr(num % 85 + 33) + enc_block
                num //= 85
            encoded += enc_block
    encoded += "~>"
    return encoded  


def encode_ascii(string):

    return [ord(c) for c in string]
    

def encode_aztec_barcode(string):

    binary_str = ''.join(format(ord(c), 'b').zfill(8) for c in string)
    binary_str_len = len(binary_str)
    if binary_str_len > 91:
        raise ValueError('Input string too long for Aztec barcode encoding.')
    elif binary_str_len > 77:
        n = 4
    elif binary_str_len > 59:
        n = 3
    elif binary_str_len > 34:
        n = 2
    else:
        n = 1
    binary_str += '0' * ((n + 1) * 2 - (binary_str_len + n) % (n + 1))
    encoded_str = ''
    while binary_str:
        if binary_str[:2] == '00':
            binary_str = binary_str[2:]
            encoded_str += 'b'
        elif binary_str[:2] == '01':
            binary_str = binary_str[2:]
            encoded_str += 'a'
        elif binary_str[:2] == '10':
            binary_str = binary_str[2:]
            if binary_str[:n] == '1' * n:
                encoded_str += 'e'
                binary_str = binary_str[n:]
            else:
                encoded_str += 'd'
                binary_str = binary_str[n:]
        else:
            binary_str = binary_str[2:]
            if binary_str[:n] == '0' * n:
                encoded_str += 'c'
                binary_str = binary_str[n:]
            else:
                encoded_str += 'b'
    return encoded_str


def encode_base32_crockford(string):

    characters = '0123456789ABCDEFGHJKMNPQRSTVWXYZ'

    binary_string = ''.join(format(ord(char), '08b') for char in string)
    while len(binary_string) % 5 != 0:
        binary_string += '0'

    encoded_string = ''
    for i in range(0, len(binary_string), 5):
        chunk = binary_string[i:i+5]
        index = int(chunk, 2)
        encoded_string += characters[index]
    
    return encoded_string


# Base32 Encoding
def encode_base32(string):

    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'
    binary_string = ''.join(format(ord(char), '08b') for char in string)
    while len(binary_string) % 5 != 0:
        binary_string += '0'

    encoded_string = ''
    for i in range(0, len(binary_string), 5):
        chunk = binary_string[i:i+5]
        index = int(chunk, 2)
        encoded_string += characters[index]
    
    return encoded_string


# Base45 Encoding
def encode_base45(string):

    characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:'

    binary_string = ''.join(format(ord(char), '08b') for char in string)
    while len(binary_string) % 5 != 0:
        binary_string += '0'

    encoded_string = ''
    for i in range(0, len(binary_string), 5):
        chunk = binary_string[i:i+5]
        index = int(chunk, 2)
        encoded_string += characters[index]
    
    return encoded_string

def encode_base58(string):

    characters = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

    binary_string = ''.join(format(ord(char), '08b') for char in string)
    while len(binary_string) % 6 != 0:
        binary_string += '0'

    encoded_string = ''
    for i in range(0, len(binary_string), 6):
        chunk = binary_string[i:i+6]
        index = int(chunk, 2)
        encoded_string += characters[index]
    
    return encoded_string


# Base62 Encoding
def encode_base62(string):
    
    characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    number = 0
    for char in string:
        number = number * 256 + ord(char)

    encoded_string = ''
    while number > 0:
        remainder = number % 62
        encoded_string = characters[remainder] + encoded_string
        number //= 62
    
    return encoded_string


# Base64 Coding
def encode_base64(string):

    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='

    binary_string = ''.join(format(ord(char), '08b') for char in string)
    while len(binary_string) % 6 != 0:
        binary_string += '0'
    
    encoded_string = ''
    for i in range(0, len(binary_string), 6):
        chunk = binary_string[i:i+6]
        index = int(chunk, 2)
        encoded_string += characters[index]
    
    return encoded_string

# Base91 Encoding
def encode_base91(string):

    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!#$%&()*+,./:;<=>?@[]^_`{|}~"'
    
    binary_string = ''.join(format(ord(char), '08b') for char in string)
    while len(binary_string) % 13 != 0:
        binary_string += '0'

    encoded_string = ''
    for i in range(0, len(binary_string), 13):
        chunk = binary_string[i:i+13]
        index = int(chunk, 2)
        quotient, remainder = divmod(index, 91*91)
        encoded_string += characters[quotient] + characters[remainder // 91] + characters[remainder % 91]
    
    return encoded_string


# Baudot Code
def encode_baudot(string):

    characters = {
        ' ': '00000',
        'A': '00011',
        'B': '11000',
        'C': '00101',
        'D': '10000',
        'E': '00100',
        'F': '01010',
        'G': '11001',
        'H': '01000',
        'I': '00010',
        'J': '10110',
        'K': '01100',
        'L': '10010',
        'M': '11100',
        'N': '10100',
        'O': '11110',
        'P': '01110',
        'Q': '11010',
        'R': '01011',
        'S': '00110',
        'T': '00111',
        'U': '01101',
        'V': '10001',
        'W': '11101',
        'X': '10011',
        'Y': '10101',
        'Z': '11011',
        '\n': '00001',  # Line feed
        '\r': '00010',  # Carriage return
    }
    
    baudot_string = ''
    for char in string.upper():
        if char in characters:
            baudot_string += characters[char]
    
    return baudot_string


# Chuck Norris Unary Code
def encode_chuck_norris(string):

    binary_string = ''.join(format(ord(char), '08b') for char in string)
    
    # Encode the binary string using Chuck Norris Unary code
    encoded_string = ''
    prev_bit = ''
    for bit in binary_string:
        if bit == '0':
            if prev_bit != '0':
                encoded_string += '00 0'
            else:
                encoded_string += '0'
        else:
            if prev_bit != '1':
                encoded_string += '00 0'
            else:
                encoded_string += '0'
            encoded_string += '0'
        prev_bit = bit
    
    return encoded_string


# EBCDIC Encoding
def encode_ebcdic(string):

    characters = {
        ' ': '40',
        '!': '5A',
        '"': '7F',
        '#': '7B',
        '$': '5B',
        '%': '6C',
        '&': '50',
        '\'': '7D',
        '(': '4D',
        ')': '5D',
        '*': '5C',
        '+': '4E',
        ',': '6B',
        '-': '60',
        '.': '4B',
        '/': '61',
        '0': 'F0',
        '1': 'F1',
        '2': 'F2',
        '3': 'F3',
        '4': 'F4',
        '5': 'F5',
        '6': 'F6',
        '7': 'F7',
        '8': 'F8',
        '9': 'F9',
        ':': '7A',
        ';': '5E',
        '<': '4C',
        '=': '7E',
        '>': '6E',
        '?': '6F',
        '@': 'C0',
        'A': 'C1',
        'B': 'C2',
        'C': 'C3',
        'D': 'C4',
        'E': 'C5',
        'F': 'C6',
        'G': 'C7',
        'H': 'C8',
        'I': 'C9',
        'J': 'D1',
        'K': 'D2',
        'L': 'D3',
        'M': 'D4',
        'N': 'D5',
        'O': 'D6',
        'P': 'D7',
        'Q': 'D8',
        'R': 'D9',
        'S': 'E2',
        'T': 'E3',
        'U': 'E4',
        'V': 'E5',
         'W': 'E6',
        'X': 'E7',
        'Y': 'E8',
        'Z': 'E9',
        '[': '7C',
        '\\': '5F',
        ']': '6D',
        '^': '79',
        '_': '5B',
        '`': '71',
        'a': '81',
        'b': '82',
        'c': '83',
        'd': '84',
        'e': '85',
        'f': '86',
        'g': '87',
        'h': '88',
        'i': '89',
        'j': '91',
        'k': '92',
        'l': '93',
        'm': '94',
        'n': '95',
        'o': '96',
        'p': '97',
        'q': '98',
        'r': '99',
        's': 'A2',
        't': 'A3',
        'u': 'A4',
        'v': 'A5',
        'w': 'A6',
        'x': 'A7',
        'y': 'A8',
        'z': 'A9',
        '{': '7B',
        '|': '7C',
        '}': '7D',
        '~': '7E'
    }
    
    encoded_string = ''
    for char in string:
        if char in characters:
            encoded_string += characters[char]
        else:
            encoded_string += characters[' ']
    
    return encoded_string


# Binary Code
def encode_binary(string):

    return ''.join(format(ord(char), '08b') for char in string)


# French Postal Barcode
def encode_french_postal(string):
  
    encoding_table = {
        '0': '3211',
        '1': '2221',
        '2': '2122',
        '3': '1411',
        '4': '1132',
        '5': '1231',
        '6': '1114',
        '7': '1312',
        '8': '1213',
        '9': '3112',
        'A': '1123',
        'B': '1222',
        'C': '2212',
        'D': '1141',
        'E': '2311',
        'F': '1321',
        'G': '4111',
        'H': '2131',
        'I': '3121',
        'J': '2113',
        'K': '2211',
        'L': '3212',
        'M': '1142',
        'N': '4112',
        'O': '2241',
        'P': '1431',
        'Q': '2421',
        'R': '1341',
        'S': '2321',
        'T': '3411',
        'U': '1332',
        'V': '1212',
        'W': '2422',
        'X': '2213',
        'Y': '2331',
        'Z': '1143',
        '-': '1112',
        '.': '3111',
        ' ': '1121'
    }
    
    encoded_string = '1'
    for char in string:
        if char in encoding_table:
            encoded_string += encoding_table[char]
        else:
            encoded_string += encoding_table[' ']
    encoded_string += '1'
    
    return encoded_string


# Gray Code
def encode_gray(string):

    def gray_code(n):
        return n ^ (n >> 1)
    
    encoded_string = ''
    for char in string:
        encoded_char = format(gray_code(ord(char)), '08b')
        encoded_string += encoded_char
    return encoded_string

# Morse Code
def encode_morse_code(string):

    encoding_table = {
        'A': '.-', 
        'B': '-...', 
        'C': '-.-.', 
        'D': '-..', 
        'E': '.', 
        'F': '..-.', 
        'G': '--.', 
        'H': '....', 
        'I': '..', 
        'J': '.---', 
        'K': '-.-', 
        'L': '.-..', 
        'M': '--', 
        'N': '-.', 
        'O': '---', 
        'P': '.--.', 
        'Q': '--.-', 
        'R': '.-.', 
        'S': '...', 
        'T': '-', 
        'U': '..-', 
        'V': '...-', 
        'W': '.--', 
        'X': '-..-', 
        'Y': '-.--', 
        'Z': '--..',
        '0': '-----',
        '1': '.----',
        '2': '..---',
        '3': '...--',
        '4': '....-',
        '5': '.....',
        '6': '-....',
        '7': '--...',
        '8': '---..',
        '9': '----.'
    }
    
    encoded_string = ''
    for char in string:
        if char.upper() in encoding_table:
            encoded_string += encoding_table[char.upper()] + ' '
        else:
            encoded_string += ' '
    return encoded_string.strip()

# BCD Encoding
def encode_bcd(string):

    encoded_string = ''
    for char in string:
        digit = int(char)
        encoded_digit = format(digit, '04b')
        encoded_string += encoded_digit
    return encoded_string

def encode_excess_3(string):
   
    if not string.isnumeric():
        raise ValueError('Input string must contain only numeric characters')
    
    encoded_string = ''
    for char in string:
        digit = int(char)
        encoded_digit = format(digit + 3, '04b')
        encoded_string += encoded_digit
    return encoded_string

def encode_resistor_value(value, tolerance):
   
    if not isinstance(value, int) or value <= 0:
        raise ValueError('Input value must be a positive integer')

    value_str = str(value).zfill(2)

    multiplier = 0
    while value >= 10:
        value /= 10
        multiplier += 1
    multiplier_str = str(multiplier)

    if tolerance == 1:
        tolerance_code = 'F'
    elif tolerance == 2:
        tolerance_code = 'G'
    elif tolerance == 5:
        tolerance_code = 'J'
    elif tolerance == 10:
        tolerance_code = 'K'
    elif tolerance == 20:
        tolerance_code = 'M'
    elif tolerance == 0.5:
        tolerance_code = 'D'
    elif tolerance == 0.25:
        tolerance_code = 'C'
    elif tolerance == 0.1:
        tolerance_code = 'B'
    elif tolerance == 0.05:
        tolerance_code = 'A'
    else:
        raise ValueError('Invalid tolerance value')
    
    color_codes = {
        '0': 'black',
        '1': 'brown',
        '2': 'red',
        '3': 'orange',
        '4': 'yellow',
        '5': 'green',
        '6': 'blue',
        '7': 'violet',
        '8': 'gray',
        '9': 'white'
    }

    encoding = color_codes[value_str[0]] + color_codes[value_str[1]] + color_codes[multiplier_str] + tolerance_code
    
    return encoding

