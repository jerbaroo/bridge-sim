import pandas as pd

filenames = ["displasensors-original.txt", "strainsensors-original.txt"]

for filename in filenames:
    df = pd.read_csv(filename, sep=" ", header=None)
    if filename == "displasensors-original.txt":
        df.columns = ["x", "z", "y", "plane", "direction", "unknown1", "label", "unknown2"]
    elif filename == "strainsensors-original.txt":
        df.columns = ["x", "z", "y", "plane", "direction", "unknown1", "label", "dist"]
    else:
        raise ValueError(f"Unknown filename {filename}")
    print(df.head())
    df["x"] = df["x"] / 1000
    df["z"] = df["z"] / 1000 - 16.6
    df["y"] = df["y"] / 1000 - 3.59
    # df.to_csv(filename.replace("-original", ""), float_format="%.3f")

    with open(filename.replace("-original", "-org"), "w") as f:
        f.write("|")
        f.write("|".join(df.columns))
        f.write("|\n|")
        f.write("|".join(map(lambda _: "--", df.columns)))
        f.write("|\n")
        for i, row in df.iterrows():
            print(row)
            f.write("|")
            f.write("|".join(map(lambda c: str(row[c]), df.columns)))
            f.write("|\n")
