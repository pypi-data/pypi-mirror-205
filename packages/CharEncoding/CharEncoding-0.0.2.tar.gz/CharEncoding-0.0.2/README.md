# Character Encoding

## Description 
List of Encoding Algorithms:

- 7-Segment Display
- ASCII85 Encoding
- ASCII Code
- Aztec Barcode
- Base-32 Crockford
- Base32
- Base45 
- Base 58
- Base62
- Base64
- ase91
- Baudot
- Binary
- Chuck Norris Unary Code
- EBCDIC Encoding
- French Postal Barcode
- Gray Code
- Morse Code
- BCD Encoding
- Excess-3 Code (Stibitz)
- Resistor Value 


## Installation

```
pip install CharEncoding
```

As usual with Pip, you might need to use `sudo` or the `--user` flag
with the command above, depending on how you installed Python on your
system.

## Usage
* Importing

```
import CharEncoding
```

* Input

```
string = 'helloworld'
stringnum = '7979'
```

* Encoding

```

print('7-Segment Display : ',CharEncoding.encode_7_segment_display(string))
print('Aztec Barcode : ' ,CharEncoding.encode_aztec_barcode(string))
print('ASCII85 Encoding : ' ,CharEncoding.encode_ascii85(string))
print('ASCII Code : ' ,CharEncoding.encode_ascii(string))
print('Base-32 Crockford : ' ,CharEncoding.encode_base32_crockford(string))
print('Base32 : ' ,CharEncoding.encode_base32(string))
print('Base45 : ' ,CharEncoding.encode_base45(string))
print('Base58 : ' ,CharEncoding.encode_base58(string))
print('Base62 : ' ,CharEncoding.encode_base62(string))
print('Base64 : ' ,CharEncoding.encode_base64(string))
print('Base91 : ' ,CharEncoding.encode_base91(string))
print('Baudot : ' ,CharEncoding.encode_baudot(string))
print('Chuck Norris Unary Code : ' ,CharEncoding.encode_chuck_norris(string))
print('EBCDIC Encoding : ' ,CharEncoding.encode_ebcdic(string))
print('Binary : ' ,CharEncoding.encode_binary(string))
print('French Postal Barcode : ' ,CharEncoding.encode_french_postal(string))
print('Gray Code : ' ,CharEncoding.encode_gray(string))
print('Morse Code : ' ,CharEncoding.encode_morse_code(string))
print('BCD Encoding : ' ,CharEncoding.encode_bcd(stringnum))
print('Excess-3 Code (Stibitz) : ' ,CharEncoding.encode_excess_3(stringnum))
print('Resistor Value  : ' ,CharEncoding.encode_resistor_value(7979, 10))

```