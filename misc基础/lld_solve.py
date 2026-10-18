from scapy.all import rdpcap, IP
from collections import Counter as _Ctr

PCAP_PATH = r"D:\lld.pcap"
NORMAL_TTL = 64


def _collect_ips(pkts):
    src_bag, dst_bag = set(), set()
    for p in pkts:
        if IP in p:
            src_bag.add(p[IP].src)
            dst_bag.add(p[IP].dst)
    return src_bag, dst_bag


def _find_internal_host(pkts):
    tally = _Ctr()
    for p in pkts:
        if IP in p:
            tally[p[IP].src] += 1
    return tally.most_common(1)[0][0]


def _sniff_ttl(pkts, host):
    records = []
    for p in pkts:
        if IP in p and p[IP].src == host:
            records.append((p[IP].ttl, p[IP].id, p[IP].dst, p.time))
    return records


def _show_stats(pkts, records):
    print("Protocol statistics:")
    print("  Total packets: {}".format(len(pkts)))
    s, d = _collect_ips(pkts)
    print("  Source IPs: {}".format(s))
    print("  Destination IPs: {}".format(d))
    host = _find_internal_host(pkts)
    print("  Internal host (most active source): {}".format(host))
    print("\n  Outbound packets: {}".format(len(records)))
    ttl_hist = _Ctr(r[0] for r in records)
    print("  TTL distribution: {}".format(dict(sorted(ttl_hist.items()))))
    return host


def _find_gaps(indices):
    return [indices[k + 1] - indices[k] for k in range(len(indices) - 1)]


def _extract(pkts, records):
    suspicious = [i for i, r in enumerate(records) if r[0] != NORMAL_TTL]
    if suspicious:
        gaps = _find_gaps(suspicious)
        print("\n  Anomalous packet indices: {}...".format(suspicious[:20]))
        print("  Gaps between anomalies: {}...".format(gaps[:20]))
        mode = _Ctr(gaps).most_common(1)[0][0] if gaps else 0
        print("  Mode gap: {} (data at every {}th packet)".format(mode, mode))

    letters = []
    print("\n  Extracting flag characters (every 5th packet):")
    for i, r in enumerate(records):
        ttl_val, ipid, dst, _ = r
        if ttl_val != NORMAL_TTL:
            sym = chr(ttl_val) if 32 <= ttl_val <= 126 else '[{}]'.format(ttl_val)
            letters.append(sym)
            print("    Packet #{}: TTL={:3d} -> '{}'  (ID={}, dst={})".format(i, ttl_val, sym, ipid, dst))
    return ''.join(letters)


def main():
    print("TASK 4: Live and Let Die - IP TTL Covert Channel")
    print()

    pkts = rdpcap(PCAP_PATH)
    host = _find_internal_host(pkts)
    records = _sniff_ttl(pkts, host)
    _show_stats(pkts, records)
    flag = _extract(pkts, records)

    print("FLAG: " + flag)
    return flag


if __name__ == "__main__":
    main()
