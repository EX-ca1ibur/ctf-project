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
    flag.append(unique_chars[np.argmax(z_scores)])

flag_str = ''.join(flag)

fig, axes = plt.subplots(2, 2, figsize=(14, 9))
demo_pos = [0, 4, 13, 26]

for i, pid in enumerate(demo_pos):
    ax = axes[i // 2][i % 2]
    mask = input_ids == pid
    chars = inputs[mask]
    traces = power[mask]
    best_char = flag_str[pid]

    for ch in np.unique(chars):
        tr = traces[chars == ch].flatten()
        if ch == best_char:
            ax.plot(tr, 'r-', linewidth=2.5, label=f"'{ch}' (correct)")
        else:
            ax.plot(tr, 'gray', linewidth=0.3, alpha=0.5)

    ax.set_title(f"Position {pid}  —  correct: '{best_char}'", fontsize=12, fontweight='bold')
    ax.set_xlabel("Time Sample")
    ax.set_ylabel("Power")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

fig.suptitle("Raw Power Traces  —  Correct (red) vs Others (gray)", fontsize=14, fontweight='bold')
fig.tight_layout()
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "1_raw_traces.png")
fig.savefig(out, dpi=200, bbox_inches='tight')
plt.close()
print(f"saved -> {out}")
