import base64 as b64

STD_ABC = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
FP = "NslSBwm6YNHHNreCNsmojw8zY9nGVzep9NoJ5LHpH3b8NKnQlB2Ca{XzIxeUyR85Y{COjRD09P4mFEAAFACZlAo0jwnGBrj7UAbwYBHDjBDEjBlMY{DWkE46YrVtaKh6ABDdVLoty{5Gjr5DMrmSNAo05DVu5NjR93m9VEDqMfHcjr5rAr2WVPo0lBVGaxA{N3mvBw8cYzbL5DHLlB8GBxrzYNo95B52N9HCIR4Ol3mcaxm3AocWkE2tArVeF{D0NxlvVrm6UElHFKmklB5CNE2tU{VtFPmp9B8WUNAtlNmUUBefyACwNR7zY9leFEwzj9nxARvDks5caoHo5sv{k{8ZYPH9aKwRABASy{HqY9vSjxAfNrBOVDA0As5EBEL7UBCZALAUj35SNKLAABmoHsocj6VUBxVp9NoSHBHDV64GU98ZjAmR5Evzl9leYweWl3lRFRv0UD4HB{X8IBv6BrDtjAl8Fwe29NoRBR4Zj9HUarmgAr5ck{DzlBAt5B76ABmf9rDkjAAGkzANNrvkjBDtY9nCaRnxMxH9ABmZAsb8NKnNy{mC5DIRl{VAUNeMMrDvBxADVs4SU92o93VoAR7zYDmEBsI7ABjwy{m09femjsIRjsm{VE4cYfeEVRBOUB8WBrmylD4GUBeAI3mvHwDOl9luFw5pY{mcVfAtlzHcjKLKU3m{MR4cjBVuFrDUNsmRMR4t5P5HU98fIAmJF{LZyfocjKLMj3ldU{8qYr88FRLflB5mBK20ArDANKAlN3m{VrmZjB59az5NANrOYzrzAKncBxVp9B5v5BmzyNVcjK46F3vvkfoKH9LGawoyMslvFLHDlElHHKADAomtNLAtUDVtaKL8Y{jw5LAtHBDmkRLRyPV{NR78YPAEVzA793vvILHKj35SFrexMrvkyLBzY3vlBx5xMrm9VBHO5DAUaRLyNACwVfAjlBeAUNeKyBDvyrH0ND48HKnxMrvkN9hzYE5AFze293CZU{Hy"
TMPL = "bctf{?????????????????????????FiXed???????????????????????p01nT}"


class AlphabetRecovery:
    def __init__(self, fp_string, tmpl):
        self.fp = fp_string
        self.mapping = dict()
        self.tmpl = list(tmpl)

    def compute_std_b64(self):
        raw_bytes = self.fp.encode()
        encoded_bytes = b64.b64encode(raw_bytes)
        text = encoded_bytes.decode()
        return text.replace('=', '')

    def fill_mapping(self, std_text):
        limit = min(len(std_text), len(self.fp))
        for idx in range(limit):
            sc = std_text[idx]
            cc = self.fp[idx]
            six_bit = STD_ABC.index(sc)
            if six_bit not in self.mapping:
                self.mapping[six_bit] = cc
                if six_bit < len(self.tmpl):
                    self.tmpl[six_bit] = cc
            elif self.mapping[six_bit] != cc:
                raise ValueError("Conflict at index {}".format(six_bit))
        return self

    def build_result(self):
        buf = ['?'] * 64
        for k in range(64):
            if k < len(self.tmpl):
                buf[k] = self.tmpl[k]
        for k, v in self.mapping.items():
            buf[k] = v
        return ''.join(buf)

    def report(self):
        std = self.compute_std_b64()
        self.fill_mapping(std)
        final = self.build_result()

        unknown = final.count('?')

        if unknown:
            blanks = [str(pos) for pos, c in enumerate(final) if c == '?']
            print("Unknown indices: [{}]".format(', '.join(blanks)))

        used_idx = sorted({STD_ABC.index(c) for c in set(std)})

        missing_idx = sorted(set(range(64)) - set(used_idx))
        print("Indices NOT used: {}".format(missing_idx))
        print("Count of unused: {}".format(len(missing_idx)))

        print("\nAlphabet (flag):")
        print(final)

        return final

    def decode(self):
        std = self.compute_std_b64()
        self.fill_mapping(std)
        alphabet = self.build_result()
        print("Alphabet (flag):")
        print(alphabet)

        rev_map = {}
        for six_bit, ch in enumerate(alphabet):
            if ch != '?':
                rev_map[ch] = six_bit

        bits = ''
        unknown = 0
        for ch in self.fp:
            if ch in rev_map:
                bits += format(rev_map[ch], '06b')
            else:
                unknown += 1

        flag_bytes = bytes(
            int(bits[i:i+8], 2) for i in range(0, len(bits) - 7, 8)
        )

        try:
            flag = flag_bytes.decode('utf-8')
            print(f"\nDecoded from FP:\n{flag}")
        except:
            print(f"\nRaw decoded bytes:\n{flag_bytes}")

        print(f"\nUnknown chars in FP: {unknown}")
        return flag_bytes


if __name__ == "__main__":
    AlphabetRecovery(FP, TMPL).decode()
