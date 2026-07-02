import os

root = r"D:\Test_git\exam_system"
for dirpath, dirnames, filenames in os.walk(root):
    for fn in filenames:
        if not fn.endswith(".py"):
            continue
        fpath = os.path.join(dirpath, fn)
        with open(fpath, "rb") as f:
            raw = f.read()
        # Fix escaped triple quotes: \"\"\" -> """
        target = b'\\"\\"\\"'
        replacement = b'"""'
        if target in raw:
            raw = raw.replace(target, replacement)
            with open(fpath, "wb") as f:
                f.write(raw)
            print(f"Fixed: {fpath}")
print("Done")
