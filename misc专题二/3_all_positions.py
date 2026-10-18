import numpy as np
from matplotlib import pyplot as plt
import os

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

data = np.load('D:/data.npz')
inputs = data['input']
input_ids = data['input_id']
power = data['power']

flag = []
details = []

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
    sorted_idx = np.argsort(z_scores)[::-1]

    flag.append(unique_chars[best_idx])
    details.append({
        'char': unique_chars[best_idx],
        'z': z_scores[best_idx],
        't': best_t,
        'r2': unique_chars[sorted_idx[1]],
        'z2': z_scores[sorted_idx[1]],
        'traces': char_traces,
        'chars': unique_chars,
    })

flag_str = ''.join(flag)

fig, axes = plt.subplots(9, 3, figsize=(18, 30))

for pid in range(27):
    ax = axes[pid // 3][pid % 3]
    d = details[pid]
    best_idx = list(d['chars']).index(d['char'])
    other = np.ones(len(d['chars']), dtype=bool)
    other[best_idx] = False

    mean_o = d['traces'][other].mean(axis=0)
    std_o = d['traces'][other].std(axis=0)
    t = np.arange(100)

    ax.fill_between(t, mean_o - std_o, mean_o + std_o, alpha=0.3, color='gray')
    ax.plot(t, mean_o, 'gray', linewidth=1.2, label='Others (mean +/- 1std)')
    ax.plot(t, d['traces'][best_idx], 'r-', linewidth=2.0, label=f"'{d['char']}' (correct)")
    ax.axvline(x=d['t'], color='blue', linestyle='--', alpha=0.5, linewidth=1)

    ax.set_title(f"Pos {pid}: '{d['char']}' Z={d['z']:.1f}  "
                 f"vs #2 '{d['r2']}' Z={d['z2']:.1f}", fontsize=9)
    ax.set_xlabel("Time")
    ax.set_ylabel("Power")
    ax.legend(fontsize=6, loc='best')
    ax.grid(True, alpha=0.2)

fig.suptitle("All 27 Positions  —  Correct Char vs Others  (blue = max-var time)",
             fontsize=14, fontweight='bold', y=0.998)
fig.tight_layout()
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "3_all_positions.png")
fig.savefig(out, dpi=150, bbox_inches='tight')
plt.close()
print(f"saved -> {out}")
