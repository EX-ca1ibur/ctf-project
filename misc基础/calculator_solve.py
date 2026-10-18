def solve_calculator(path):
    raw = open(path, 'r', encoding='utf-8').readlines()

    result_parts = []
    linenum = 79
    while linenum < min(112, len(raw)):
        cur = raw[linenum].rstrip('\n\r')
        linenum = linenum + 1

        if cur == '\t' or len(cur) == 0:
            continue

        binary_text = ''
        tab_hits = 0
        space_hits = 0
        for symbol in cur:
            if symbol == '\t':
                binary_text = binary_text + '1'
                tab_hits = tab_hits + 1
            else:
                binary_text = binary_text + '0'
                space_hits = space_hits + 1

        number = int(binary_text, base=2)
        letter = chr(number)
        result_parts.append(letter)

        print("Line %d: %s (%d bits) -> %d -> '%s'  tabs=%d spaces=%d" %
              (linenum, binary_text, len(binary_text), number, letter, tab_hits, space_hits))

    answer = ''
    for part in result_parts:
        answer = answer + part



    print("FLAG: " + answer)

    return answer


if __name__ == "__main__":
    solve_calculator(r"D:\calculator.lua")
