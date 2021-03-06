"""Test that examples in the README are runnable.

The one true source of these examples is example.py. It is these examples that
will be tested. A second test will check that the examples in the README are the
same as in example.py.

"""

import shutil
import os
import subprocess
from collections import defaultdict
from typing import Dict, List

from bridge_sim import configs


def read_examplepy_examples() -> Dict[int, List[str]]:
    """Read examples from the example.py file.

    Returns:
        dictionary of example index to lines of Python code.

    """
    curr_example = 0
    lines_per_example = defaultdict(list)
    with open("example.py") as f:
        lines = f.readlines()
    for line in lines:
        if f"Example {curr_example + 1}" in line:
            curr_example += 1
        lines_per_example[curr_example].append(line)
    return lines_per_example


def read_readme_examples() -> Dict[int, List[str]]:
    """Read examples from the README.org file.

    Returns:
        dictionary of example index to lines of Python code.

    """
    curr_example = 0
    in_example = False
    lines_per_example = defaultdict(list)
    with open("README.org") as f:
        lines = f.readlines()
    for line in lines:
        if line.startswith(f"*** Example {curr_example + 1}"):
            curr_example += 1
        if line.startswith("#+BEGIN_SRC"):
            in_example = True
        if line.startswith("#+END_SRC"):
            in_example = False
        if in_example:
            lines_per_example[curr_example].append(line)
    return lines_per_example


def test_example_py():
    """Run each example, unless it has contains NOTEST comment."""
    c, exe_found = configs.test_config(msl=10)
    if not exe_found:
        return
    temp_example_name = "rm-example.py"
    temp_image_name = "rm-image.png"
    temp_data_dir = "rm-test-data"

    def remove():
        """Remove data generated by this test."""
        if os.path.exists(temp_image_name):
            os.remove(temp_image_name)
        if os.path.exists(temp_example_name):
            os.remove(temp_example_name)
        if os.path.exists(temp_data_dir):
            shutil.rmtree(temp_data_dir)

    remove()
    lines_per_example = read_examplepy_examples()
    try:
        for index, lines in lines_per_example.items():
            if index == 0 or any("NOPYTEST" in l for l in lines):
                continue
            # Write the resulting file with two adjustments:
            # - save generated data to a specific folder for this test
            for l_i, line in enumerate(lines):
                if "opensees_default" in line:
                    line = line.strip()[:-1]  # Remove last ')'
                    line += f", generated_data='{temp_data_dir}')\n"
                lines[l_i] = line
            # - save the generated image instead of showing it
            with open(temp_example_name, "w") as f:
                f.write("".join(lines).replace(
                    "plt.show()",
                    f"plt.savefig('{temp_image_name}')",
                ))
            result = subprocess.run(
                ["poetry", "run", "python", temp_example_name]
            )
            assert result.returncode == 0
    finally:
        remove()


def test_readme():
    """Test that examples in the README are the same as in example.py."""
    lines_per_example_e = read_examplepy_examples()
    lines_per_example_r = read_readme_examples()
    indexes = sorted(set(
        list(lines_per_example_e.keys()) + list(lines_per_example_r.keys())
    ))
    indexes.remove(0)  # First example is number 1.

    def rm_lines(ls):
        """Ignore whitespace and comment lines."""
        return [
            l for l in ls if not
            (l.startswith("#") or l.strip() == "")
        ]

    for i in indexes:
        lines_e = rm_lines(lines_per_example_e[i])
        lines_r = rm_lines(lines_per_example_r[i])
        for (line_e, line_r) in zip(lines_e, lines_r):
            if line_e != line_r:
                raise Exception(
                    f"Example {i} lines NOT equal, example.py then README.org:"
                    f"\n\n{line_e}\n{line_r}"
                )
