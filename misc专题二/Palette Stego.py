import struct
import zlib


def extract_ezstego(png_path):
    with open(png_path, 'rb') as f:
        data = f.read()

    pos = 8
    palette = b''
    idat_data = b''
    width = height = 0

    while pos < len(data):
        length = struct.unpack('>I', data[pos:pos + 4])[0]
        chunk_type = data[pos + 4:pos + 8].decode('ascii')
        chunk_data = data[pos + 8:pos + 8 + length]

        if chunk_type == 'IHDR':
            width = struct.unpack('>I', chunk_data[0:4])[0]
            height = struct.unpack('>I', chunk_data[4:8])[0]
        elif chunk_type == 'PLTE':
            palette = chunk_data
        elif chunk_type == 'IDAT':
            idat_data += chunk_data
        elif chunk_type == 'IEND':
            break

        pos += 12 + length

    raw = zlib.decompress(idat_data)

    pixels = bytearray()
    for y in range(height):
        row_start = y * (1 + width)
        filter_type = raw[row_start]
        row_data = raw[row_start + 1:row_start + 1 + width]

        if filter_type == 0:
            pixels.extend(row_data)
        elif filter_type == 1:
            decoded = bytearray(row_data)
            for x in range(width):
                left = decoded[x - 1] if x > 0 else 0
                decoded[x] = (row_data[x] + left) & 0xFF
            pixels.extend(decoded)
        elif filter_type == 2:
            decoded = bytearray(row_data)
            for x in range(width):
                up = pixels[(y - 1) * width + x] if y > 0 else 0
                decoded[x] = (row_data[x] + up) & 0xFF
            pixels.extend(decoded)
        elif filter_type == 3:
            decoded = bytearray(row_data)
            for x in range(width):
                left = decoded[x - 1] if x > 0 else 0
                up = pixels[(y - 1) * width + x] if y > 0 else 0
                decoded[x] = (row_data[x] + (left + up) // 2) & 0xFF
            pixels.extend(decoded)
        elif filter_type == 4:
            decoded = bytearray(row_data)
            for x in range(width):
                a = decoded[x - 1] if x > 0 else 0
                b = pixels[(y - 1) * width + x] if y > 0 else 0
                c = pixels[(y - 1) * width + x - 1] if (y > 0 and x > 0) else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pr = a if pa <= pb and pa <= pc else (b if pb <= pc else c)
                decoded[x] = (row_data[x] + pr) & 0xFF
            pixels.extend(decoded)

    n = len(palette) // 3
    colors = []
    for i in range(n):
        r, g, b = palette[i * 3], palette[i * 3 + 1], palette[i * 3 + 2]
        colors.append((i, 0.299 * r + 0.587 * g + 0.114 * b))

    sorted_colors = sorted(colors, key=lambda x: x[1])

    idx_to_pos = {}
    for pos, (idx, _) in enumerate(sorted_colors):
        idx_to_pos[idx] = pos

    bits = []
    for p in pixels:
        bits.append(str(idx_to_pos[p] & 1))

    bit_string = ''.join(bits)

    byte_list = []
    for i in range(len(bit_string) // 8):
        byte_list.append(int(bit_string[i * 8:(i + 1) * 8], 2))
    text = bytes(byte_list)

    for prefix in [b'flag{', b'AAA{', b'FLAG{']:
        p = text.find(prefix)
        if p != -1:
            end = text.find(b'}', p)
            if end != -1:
                return text[p:end + 1].decode()

    return ''


if __name__ == '__main__':
    flag = extract_ezstego(r'D:\palette.png')
    print(flag)
