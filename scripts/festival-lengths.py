"""Regenerate the draft's charts: uv run --with matplotlib scripts/festival-lengths.py."""

import csv
import statistics
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

BUNDLE = Path(__file__).resolve().parents[1] / "rnp/content/posts/2026-11-05-liff26-in-numbers"


def load(name):
    with (BUNDLE / name).open(encoding="utf-8", newline="") as handle:
        return [int(row["minutes"]) for row in csv.DictReader(handle)]


def histogram(lengths, title, filename, edges):
    fig, ax = plt.subplots(figsize=(10, 6), layout="constrained")
    counts, bins, _ = ax.hist(lengths, bins=edges, color="#337ba3", edgecolor="white")
    for count, left, right in zip(counts, bins[:-1], bins[1:]):
        if count:
            ax.text((left + right) / 2, count + 0.15, str(int(count)), ha="center")
    mean, median = statistics.mean(lengths), statistics.median(lengths)
    ax.axvline(mean, color="#c14827", linestyle="--", label=f"Mean: {mean:.1f} min")
    ax.axvline(median, color="#333b44", linestyle=":", label=f"Median: {median:g} min")
    ax.set_title(f"{title}\n{len(lengths)} titles / programmes", loc="left", fontsize=17)
    ax.set_xticks([(left + right) / 2 for left, right in zip(edges[:-1], edges[1:])])
    ax.set_xlabel("Length (minutes); 10-minute buckets centred on multiples of 10")
    ax.set_ylabel("Number of titles / programmes")
    ax.set_ylim(0, max(counts) * 1.18)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False)
    fig.savefig(BUNDLE / filename, dpi=160)
    plt.close(fig)


mine = load("selection-lengths.csv")
festival = load("catalogue-lengths.csv")
histogram(mine, "My LIFF 2026 selection", "selection-lengths.png", list(range(65, 146, 10)))
edges = list(range(55, 206, 10))
histogram(festival, "LIFF 2026 catalogue", "catalogue-lengths.png", edges)
centres = [(left + right) / 2 for left, right in zip(edges[:-1], edges[1:])]
my_percent = [100 * sum(left <= n < right for n in mine) / len(mine)
              for left, right in zip(edges[:-1], edges[1:])]
festival_percent = [100 * sum(left <= n < right for n in festival) / len(festival)
                    for left, right in zip(edges[:-1], edges[1:])]
fig, ax = plt.subplots(figsize=(12, 6), layout="constrained")
ax.bar([n - 2 for n in centres], my_percent, width=4, color="#337ba3", label=f"My selection (n={len(mine)})")
ax.bar([n + 2 for n in centres], festival_percent, width=4, color="#df8a50", label=f"Festival catalogue (n={len(festival)})")
ax.set_title("My selection vs the full festival catalogue", loc="left", fontsize=17)
ax.set_xticks(centres)
ax.set_xlabel("Length (minutes); 10-minute buckets centred on multiples of 10")
ax.set_ylabel("Percentage of titles / programmes")
ax.spines[["top", "right"]].set_visible(False)
ax.legend(frameon=False)
fig.savefig(BUNDLE / "lengths-comparison.png", dpi=160)
plt.close(fig)
