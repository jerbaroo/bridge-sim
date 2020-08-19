with open("example.py") as f:
    lines = f.readlines()
lines = ["from pathlib import Path\n"] + lines
example_no, last_line_ind_example_1 = 1, None
for i, line in enumerate(lines):
    if "plt.show()" in line:
        lines[i] = line.replace(
            "plt.show()",
            f"plt.savefig(Path(\"~/example-{example_no}.png\").expanduser().as_posix())",
        )
        if example_no == 1:
            last_line_ind_example_1 = i
        example_no += 1
lines.insert(last_line_ind_example_1 + 1, "import sys; sys.exit()")
with open("example.py", "w") as f:
    f.write("".join(lines))
