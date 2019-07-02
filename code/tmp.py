import sys

with open("strains_paths.tb") as f:
    lines = f.readlines()

print(len(lines))
print(sys.getsizeof(lines)/len(lines))
