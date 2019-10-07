import sys
 
with open(sys.argv[1]) as f:
    lines = f.read()

nums = list(map(float, lines.split()))
print(min(nums), max(nums))
