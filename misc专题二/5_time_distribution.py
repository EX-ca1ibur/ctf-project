import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Patch
import os

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

data = np.load('D:/data.npz')
inputs = data['input']
input_ids = data['input_id']
power = data['power']

flag = []
best_ts = []

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
    best_ts.append(best_t)

flag_str = ''.join(flag)

fig, ax = plt.subplots(figsize=(14, 5))
x = np.arange(27)

palette = ['#e74c3c'] * 20 + ['#3498db'] * 30 + ['#2ecc71'] * 30 + ['#f39c12'] * 20
colors = [palette[t] for t in best_ts]

ax.bar(x, best_ts, color=colors, alpha=0.85, edgecolor='white', linewidth=0.5)
ax.set_xticks(x)
ax.set_xticklabels([flag_str[i] for i in x], fontsize=11)
ax.set_ylabel('t_max (Time Point of Max Variance)', fontsize=11)
ax.set_title('Maximum Variance Time Point at Each Position', fontsize=13, fontweight='bold')

for i, (px, py) in enumerate(zip(x, best_ts)):
    ax.text(px, py + 1.5, str(py), ha='center', fontsize=7, color='#2c3e50')

legend_elements = [
    Patch(facecolor='#e74c3c', label='Early      (t = 0-19)'),
    Patch(facecolor='#3498db', label='Mid-early  (t = 20-49)'),
    Patch(facecolor='#2ecc71', label='Mid-late   (t = 50-79)'),
    Patch(facecolor='#f39c12', label='Late       (t = 80-99)'),
]
ax.legend(handles=legend_elements, loc='upper right', fontsize=9)

mean_t = np.mean(best_ts)
ax.axhline(y=mean_t, color='purple', linestyle=':', linewidth=1.5, alpha=0.7)
ax.text(26.5, mean_t + 1, f'Mean = {mean_t:.1f}', fontsize=9, color='purple')
ax.set_ylim(0, max(best_ts) + 8)
ax.grid(True, alpha=0.3, axis='y')

fig.suptitle("Distribution of Max-Variance Time Points", fontsize=14, fontweight='bold')
fig.tight_layout()
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "5_time_distribution.png")
fig.savefig(out, dpi=200, bbox_inches='tight')
plt.close()
print(f"saved -> {out}")
