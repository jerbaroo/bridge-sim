"""Test examples in the README work.

The one true source of these examples is in example.py. It is these examples
that will be tested. A second test will check that the examples in the README
are the same as in example.py.

"""
import os
import subprocess
from collections import defaultdict
from typing import Dict, List


def read_examples() -> Dict[int, List[str]]:
    """A dictionary of example index to lines of Python code."""
    curr_example = 0
    lines_per_example = defaultdict(list)
    with open("example.py") as f:
        lines = f.readlines()
    for line in lines:
        if f"Example {curr_example + 1}" in line:
            curr_example += 1
        lines_per_example[curr_example].append(line)
    return lines_per_example


def test_example_py():
    """Run each example, unless it has contains NOTEST comment."""
    temp_example_name, temp_image_name = "temp_example.py", "temp-image.png"
    lines_per_example = read_examples()
    for index, lines in lines_per_example.items():
        if index == 0 or any("NOTEST" in l for l in lines):
            continue
        with open(temp_example_name, "w") as f:
            f.write("".join(lines).replace(
                "plt.show()",
                f"plt.savefig({temp_image_name})",
            ))
        result = subprocess.run(["poetry", "run", "python", temp_example_name])
        assert result.returncode == 0
    if os.path.exists(temp_image_name):
        os.remove(temp_image_name)
    if os.path.exists(temp_example_name):
        os.remove(temp_example_name)


def test_readme():
    pass
