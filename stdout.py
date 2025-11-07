import os
import re

def smartFilename(filepath: str, **params) -> str:
    """
    Given a target filepath, e.g., "example.csv",
    if it already exists, it will automatically append _1, _2, etc. to ensure uniqueness.
    
    If additional **params are passed, they will be appended to the filename:
    unique_filename("out.csv", stock_X="AAPL", window=20)
    This may output "out_stock_X-AAPL_window-20.csv" or with a sequence number:
    "out_stock_X-AAPL_window-20_1.csv"
    """
    base, ext = os.path.splitext(filepath)
    # For a file named "example.csv", base = "example", ext = ".csv"
    
    if params:
        # Convert params into legal filename characters
        safe = lambda s: re.sub(r'[^0-9A-Za-z\-]+', '_', str(s))
        parts = [f"{safe(k)}-{safe(v)}" for k, v in sorted(params.items())]
        base = base + "_" + "_".join(parts)
    
    # Check if the file already exists
    # if it does, append a number to the filename
    # e.g., "example_1.csv", "example_2.csv", etc.
    counter = 1
    newpath = f"{base}{ext}"
    while os.path.exists(newpath):
        newpath = f"{base}_{counter}{ext}"
        counter += 1
    return newpath


if __name__ == "__main__":
    import pandas as pd

    df = pd.DataFrame({
        "pair":        ["A-B", "C-D", "E-F"],
        "performance": [0.95, 0.85, 0.90]
    })

    # 1.. By default, it will just add a number to the filename
    out1 = smartFilename("pairs_performance.csv")
    df.to_csv(out1, index=False)
    print("Write as:", out1)
    
    # 2.. If you provide additional parameters, they will be included in the filename
    out2 = smartFilename(
        "pairs_performance.csv",
        stock_X="AAPL",
        stock_Y="MSFT",
        window=120,
        exit_ratio=0.75
    )
    df.to_csv(out2, index=False)
    print("Write as", out2)
