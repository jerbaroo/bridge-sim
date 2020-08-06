with open("example.py") as f:
    lines = f.readlines()
lines = ["from pathlib import Path"] + lines
example_no = 1
for i, line in enumerate(lines):
    if "plt.show()" in line:
        lines[i] = line.replace(
            "plt.show()",
            f"plt.savefig(Path(\"~/docker-{example_no}.png\").expanduser().as_posix())",
        )
        example_no += 1
with open("example.py", "w") as f:
    f.write("".join(lines))
