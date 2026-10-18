import numpy as np
from matplotlib import pyplot as plt
import os

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

data = np.load('D:/data.npz')
inputs = data['input']
input_ids = data['input_id']
power = data['power']

pid = 0
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

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.plot(variances, 'b-', linewidth=1.5)
ax1.axvline(x=best_t, color='r', linestyle='--', linewidth=2, label=f'Max variance at t={best_t}')
ax1.set_title(f"Variance vs Time  (Position 0)", fontsize=12, fontweight='bold')
ax1.set_xlabel("Time Sample")
ax1.set_ylabel("Variance")
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)

colors = ['#e74c3c' if i == best_idx else '#5b9bd5' for i in range(len(unique_chars))]
ax2.bar(range(len(unique_chars)), col, color=colors, alpha=0.85)
ax2.axhline(y=col.mean(), color='gray', linestyle='-', linewidth=1.5, label=f'Mean = {col.mean():.4f}')
ax2.axhline(y=col.mean() + 2 * col.std(), color='orange', linestyle='--', linewidth=1, label='+2 Std')
ax2.axhline(y=col.mean() - 2 * col.std(), color='orange', linestyle='--', linewidth=1, label='-2 Std')
ax2.set_xticks(range(0, len(unique_chars), 3))
ax2.set_xticklabels([unique_chars[j] for j in range(0, len(unique_chars), 3)])
ax2.set_title(f"Power at t={best_t}  (correct='{best_char}', Z={z_scores[best_idx]:.1f})",
              fontsize=12, fontweight='bold')
ax2.set_xlabel("Character")
ax2.set_ylabel("Power")
ax2.legend(fontsize=9)
ax2.grid(True, alpha=0.3, axis='y')

fig.suptitle("Max-Variance Analysis Principle  (Position 0 Demo)", fontsize=14, fontweight='bold')
fig.tight_layout()
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "2_variance_principle.png")
fig.savefig(out, dpi=200, bbox_inches='tight')
plt.close()
print(f"saved -> {out}")
