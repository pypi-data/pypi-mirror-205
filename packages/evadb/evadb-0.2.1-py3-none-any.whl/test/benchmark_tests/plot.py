from textwrap import wrap
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pylab as pylab


YLABEL = "Reuse percentange"
COLOR = ["#82C0CC", "#3f72af", "#FFA62B", "#809A6F", "#A25B5B"]
COLOR = ["#82C0CC", "#3f72af", "#FFA62B", "#C9BBCF", "#898AA6"]
HATCH = ["x", "o", "^"]
FONTSIZE = 12
LABEL_FONT = FONTSIZE
import matplotlib.pylab as pylab

params = {
    "legend.fontsize": FONTSIZE,
    "figure.figsize": (5,3),
    "axes.labelsize": LABEL_FONT,
    "axes.titlesize": FONTSIZE,
    "xtick.labelsize": LABEL_FONT,
    "ytick.labelsize": LABEL_FONT,
}
pylab.rcParams.update(params)


# Avoid type 3 font
# matplotlib.rcParams['pdf.fonttype'] = 42
# matplotlib.rcParams['ps.fonttype'] = 42

matplotlib.rcParams["font.family"] = "sans-serif"
# matplotlib.rcParams["font.sans-serif"] = ["DejaVu Sans"]
# plt.rcParams.update({'font.sans-serif':'Helvetica'})


# Data
x = ["Baseline", "+Caching", "+Caching \n +Pred Reordering"]
y = [167.68, 90.24, 25.76]


# Create bar plot
plt.bar(x, y, color="#1f77b4")
plt.grid(axis="y", linestyle="-", alpha=0.5, zorder=-1)
plt.xticks(rotation=0)

plt.gca().set_axisbelow(True)
# Add labels and title
# plt.xlabel("Category")
plt.ylabel("Time (s)")
plt.title("Comparison of Query Performance with EVA")

plt.savefig(
    "/nethome/gkakkar7/VDBMS/eva/data/assets/eva_performance_comparison.png",
    dpi=500,
    bbox_inches="tight",
    transparent=True
)
