import os

months = ["jan", "feb", "march", "april", "may", "june", "july", "aug", "sep", "oct", "nov", "dec"]

lines = []
for month in months:
    with open(month + ".txt") as f:
        month_lines = f.readlines()
    lines += month_lines
with open("2018.txt", "w") as f:
    f.writelines(lines)
