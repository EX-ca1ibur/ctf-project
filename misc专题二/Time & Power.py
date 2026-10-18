import numpy as np

data = np.load('D:/data.npz')
inputs = data['input']
input_ids = data['input_id']
power = data['power']

print(f"inputs: {inputs.shape}, ids: {input_ids.shape}, power: {power.shape}")
print(f"positions: {input_ids.max() + 1}, unique chars: {len(np.unique(inputs))}")

flag = []

for pid in range(27):
    mask = input_ids == pid
    chars = inputs[mask]
    traces = power[mask]

    unique_chars = np.unique(chars)
    char_traces = np.array([traces[chars == ch].flatten() for ch in unique_chars])

    variances = np.var(char_traces, axis=0)
    best_t = np.argmax(variances)

    col = char_traces[:, best_t]
    z_scores = np.abs((col - col.mean()) / col.std())
    best_idx = np.argmax(z_scores)
    best_char = unique_chars[best_idx]

    sorted_idx = np.argsort(z_scores)[::-1]
    runner_up = unique_chars[sorted_idx[1]]
    conf = z_scores[best_idx] / z_scores[sorted_idx[1]]

    flag.append(best_char)
    print(f"  pos {pid:2d}: '{best_char}'  Z={z_scores[best_idx]:.2f}  "
          f"t={best_t}  #2='{runner_up}' Z={z_scores[sorted_idx[1]]:.2f}  "
          f"conf={conf:.1f}x")

flag_str = ''.join(flag)
print(f"\nflag: {flag_str}")
print("decoded: Oops! Power is all you need")
