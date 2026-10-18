#!/usr/bin/env python3
"""
Zero-Width Character Steganography Encoder/Decoder

This script demonstrates how attackers hide invisible instructions in files
read by AI coding agents. It encodes ASCII text using zero-width Unicode
characters that are invisible to human reviewers but processed by LLMs.

Encoding scheme:
  - U+200B (Zero Width Space)  → bit 0
  - U+200C (Zero Width Non-Joiner) → bit 1

Each character of the secret message is converted to its 8-bit binary
representation, then each bit is mapped to the corresponding zero-width
character.

This is the SAME technique used in:
  - a known supply chain attack (May 2026, 34+ malicious packages)
  - a known incident incident (35,800+ compromised IDE extensions)
  - Cursor rules injection attacks (researchers, March 2025)

Usage:
  python zw_encode.py encode "secret message" > encoded.txt
  python zw_encode.py decode encoded.txt
"""

import sys

ZWSP = '​'   # Zero Width Space = bit 0
ZWNJ = '‌'   # Zero Width Non-Joiner = bit 1

# Sentinel markers to mark start/end of hidden message
START_MARKER = ZWSP * 4 + ZWNJ * 4  # 00001111
END_MARKER = ZWNJ * 4 + ZWSP * 4    # 11110000


def char_to_zw(c: str) -> str:
    """Convert a single ASCII character to zero-width representation."""
    binary = format(ord(c), '08b')
    return ''.join(ZWSP if b == '0' else ZWNJ for b in binary)


def encode(secret: str) -> str:
    """Encode a secret message into zero-width characters."""
    result = START_MARKER
    for c in secret:
        result += char_to_zw(c)
    result += END_MARKER
    return result


def decode(text: str) -> str:
    """Extract a hidden message from text containing zero-width characters."""
    # Extract only zero-width characters
    zw_chars = ''.join(c for c in text if c in (ZWSP, ZWNJ))

    # Find start marker
    start_idx = zw_chars.find(START_MARKER)
    if start_idx == -1:
        return "[No start marker found]"

    # Find end marker
    end_idx = zw_chars.find(END_MARKER, start_idx + len(START_MARKER))
    if end_idx == -1:
        # Try to decode without end marker
        payload = zw_chars[start_idx + len(START_MARKER):]
    else:
        payload = zw_chars[start_idx + len(START_MARKER):end_idx]

    # Decode 8 bits at a time
    result = ''
    for i in range(0, len(payload) - 7, 8):
        byte_bits = payload[i:i+8]
        if len(byte_bits) < 8:
            break
        byte_str = ''.join('0' if c == ZWSP else '1' for c in byte_bits)
        result += chr(int(byte_str, 2))

    return result


def extract_all(text: str) -> list:
    """Extract ALL zero-width sequences (including those without markers)."""
    zw_chars = ''.join(c for c in text if c in (ZWSP, ZWNJ))
    return zw_chars


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python zw_encode.py encode <secret>    - encode a message")
        print("  python zw_encode.py decode <text>      - decode from text")
        print("  python zw_encode.py encode <secret>    - encode to stdout")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'encode':
        if len(sys.argv) < 3:
            secret = input("Enter secret message: ")
        else:
            secret = sys.argv[2]
        print(encode(secret))

    elif command == 'decode':
        if len(sys.argv) < 3:
            text = input("Enter text with hidden message: ")
        else:
            text = sys.argv[2]
        print("Hidden message:", decode(text))

    elif command == 'show':
        # Show the zero-width characters in a string (for debugging)
        text = sys.argv[2] if len(sys.argv) > 2 else input("Enter text: ")
        for i, c in enumerate(text):
            if c in (ZWSP, ZWNJ):
                name = 'ZWSP(0)' if c == ZWSP else 'ZWNJ(1)'
                print(f"  Position {i}: {name} U+{ord(c):04X}")
        print(f"\nTotal zero-width chars: {sum(1 for c in text if c in (ZWSP, ZWNJ))}")

    else:
        print(f"Unknown command: {command}")
