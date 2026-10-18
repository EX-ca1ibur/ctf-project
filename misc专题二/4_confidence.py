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
z_best, z_runner, confs = [], [], []

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
    z_best.append(z_scores[best_idx])
    z_runner.append(z_scores[sorted_idx[1]])
    confs.append(z_scores[best_idx] / z_scores[sorted_idx[1]])

flag_str = ''.join(flag)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8))
x = np.arange(27)
w = 0.35

ax1.bar(x - w/2, z_best, w, color='#e74c3c', alpha=0.9, label='Correct Char Z-score')
ax1.bar(x + w/2, z_runner, w, color='#95a5a6', alpha=0.9, label='Runner-up Z-score')
ax1.axhline(y=3.0, color='orange', linestyle='--', linewidth=1.5, label='3-sigma')
ax1.set_xticks(x)
ax1.set_xticklabels([flag_str[i] for i in x])
ax1.set_ylabel('|Z-score|')
ax1.set_title('Z-score: Correct Character vs Runner-up', fontsize=12, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3, axis='y')
for i in x:
    ax1.text(i - w/2, z_best[i] + 0.1, f'{z_best[i]:.1f}', ha='center', fontsize=6, color='#c0392b')
    ax1.text(i + w/2, z_runner[i] + 0.1, f'{z_runner[i]:.1f}', ha='center', fontsize=6, color='#7f8c8d')

ax2.bar(x, confs, color='#3498db', alpha=0.9)
ax2.axhline(y=2.0, color='orange', linestyle='--', linewidth=1.5, label='2x threshold')
ax2.set_xticks(x)
ax2.set_xticklabels([flag_str[i] for i in x])
ax2.set_ylabel('Confidence Ratio')
ax2.set_title('Confidence Ratio (Correct / Runner-up)', fontsize=12, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3, axis='y')
for i in x:
    ax2.text(i, confs[i] + 0.1, f'{confs[i]:.1f}x', ha='center', fontsize=7, color='#2980b9')

fig.suptitle("Analysis Confidence Summary", fontsize=14, fontweight='bold')
fig.tight_layout()
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "4_confidence_summary.png")
fig.savefig(out, dpi=200, bbox_inches='tight')
plt.close()
print(f"saved -> {out}")
