import pandas as pd
import glob
import io
import re
import os

# Get all CSV files except final_output.csv
csv_files = [f for f in glob.glob("../data/*.csv") if "final_output" not in f]
print("Found CSV files:", csv_files)

dfs = []

for file in csv_files:
    print(f"\nProcessing: {file}")

    # --- FIX BROKEN CSV LINES ---
    cleaned_rows = []
    with open(file, "r", encoding="utf-8") as f:
        raw = f.read()

        # Split where header repeats inside file
        parts = raw.split("product,price,quantity,date,region")

        for part in parts:
            part = part.strip()
            if not part:
                continue

            # Rebuild complete CSV block
            block = "product,price,quantity,date,region\n" + part
            cleaned_rows.append(block)

    final_cleaned_text = "\n".join(cleaned_rows)

    # Read cleaned CSV text properly using io.StringIO
    df = pd.read_csv(io.StringIO(final_cleaned_text))

    # Normalize product
    df["product"] = df["product"].str.lower().str.strip()

    # Filter only pink morsel
    df = df[df["product"] == "pink morsel"]

    # Clean $ sign from price and convert to float
    df["price"] = df["price"].str.replace("$", "", regex=False).astype(float)

    # Calculate sales
    df["sales"] = df["price"] * df["quantity"]

    # Keep only the required columns
    df = df[["sales", "date", "region"]]

    print("Rows kept:", len(df))
    dfs.append(df)

# Concatenate all results
final_df = pd.concat(dfs, ignore_index=True)

# Save output
output_path = "../data/final_output.csv"
final_df.to_csv(output_path, index=False)

print(f"\nDone! File created: {output_path}")
