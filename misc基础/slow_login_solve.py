from scapy.all import rdpcap, Raw, TCP, IP
from re import search
from urllib.parse import unquote_plus

DELAY_LIMIT = 0.5

RE_LEN = r'LENGTH\(\(SELECT\s+secret_value\s+FROM\s+secret_store\s+LIMIT\s+1\)\)>(\d+)'
RE_ASC = r'ASCII\(SUBSTRING\(\(SELECT\s+secret_value\s+FROM\s+secret_store\s+LIMIT\s+1\),(\d+),1\)\)>(\d+)'


def read_pcap_traffic(pcap_file):
    all_packets = rdpcap(pcap_file)
    collection = []
    idx = 0
    total = len(all_packets)
    while idx < total:
        p = all_packets[idx]
        has_payload = p.haslayer(Raw)
        has_tcp = p.haslayer(TCP)
        if has_payload and has_tcp and p[TCP].dport == 80:
            content = p[Raw].load
            if b'POST /login' not in content:
                idx += 1
                continue
            answer = None
            j = idx + 1
            while j < min(idx + 10, total):
                if all_packets[j].haslayer(Raw) and all_packets[j][TCP].sport == 80:
                    answer = all_packets[j]
                    break
                j += 1
            gap = 0.0
            if answer is not None:
                gap = answer.time - p.time
            boundary = content.find(b'\r\n\r\n')
            if boundary >= 0:
                payload_encoded = content[boundary + 4:]
            else:
                payload_encoded = b''
            decoded_body = unquote_plus(payload_encoded.decode('utf-8', errors='replace'))
            triggered = gap > DELAY_LIMIT
            collection.append(dict(
                src_port=p[TCP].sport,
                form_data=decoded_body,
                response_delay=gap,
                sleep_hit=triggered
            ))
        idx += 1
    return collection


def extract_length_value(form):
    hit = search(RE_LEN, form)
    if hit is not None:
        return int(hit.group(1))
    return None


def extract_ascii_info(form):
    hit = search(RE_ASC, form)
    if hit is not None:
        char_pos = int(hit.group(1))
        threshold_val = int(hit.group(2))
        return char_pos, threshold_val
    return None, None


def recover_flag(all_sessions):

    len_checks = []
    for entry in all_sessions:
        len_bound = extract_length_value(entry['form_data'])
        if len_bound is not None:
            len_checks.append((len_bound, entry['sleep_hit']))
            label = 'TRUE (SLEEP)' if entry['sleep_hit'] else 'FALSE'

    lower = 0
    upper = 128
    for bound, is_true in len_checks:
        if is_true:
            lower = max(lower, bound + 1)
        else:
            upper = min(upper, bound)
    secret_size = lower


    password = ['?'] * secret_size
    by_position = {}
    for entry in all_sessions:
        pos, threshold_val = extract_ascii_info(entry['form_data'])
        if pos is not None:
            if pos not in by_position:
                by_position[pos] = []
            by_position[pos].append((threshold_val, entry['sleep_hit'], entry['response_delay']))

    for pos in sorted(by_position.keys()):
        group = by_position[pos]
        lo = 31
        hi = 127
        for thr, is_hit, _ in group:
            if is_hit:
                lo = max(lo, thr + 1)
            else:
                hi = min(hi, thr)
        letter = chr(lo) if 32 <= lo <= 126 else '[%d]' % lo
        if pos <= len(password):
            password[pos - 1] = letter
        tokens = []
        for thr, is_hit, _ in group:
            tokens.append(">%d=%s" % (thr, '+' if is_hit else '-'))
        trace_line = ' '.join(tokens)

    final_secret = ''.join(password)

    print("Full secret value: " + final_secret)

    return final_secret


if __name__ == "__main__":

    print()

    all_entries = read_pcap_traffic(r"D:\slow-login.pcap")

    for e in all_entries:
        if 'SLEEP' not in e['form_data']:
            print("  " + e['form_data'])

    attack_entries = [e for e in all_entries if 'SLEEP' in e['form_data']]
    print("\nSQL injection sessions: %d" % len(attack_entries))

    result = recover_flag(attack_entries)

