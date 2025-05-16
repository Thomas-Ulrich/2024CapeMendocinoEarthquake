import pandas as pd
import argparse

parser = argparse.ArgumentParser(
    description="Compute weighted misfit from a misfit file."
)
parser.add_argument("filename", type=str, help="Path to the misfit file")

args = parser.parse_args()
filename = args.filename


df = pd.read_csv(args.filename, sep="\s+")

# Check the first few rows
print(df.head())

# Group by 'component' and compute sum(weight * misfit)
df["weighted_misfit"] = df["weight"] * df["misfit"]
misfit_by_component = df.groupby("component")["weighted_misfit"].sum()

# Print the result
print(misfit_by_component)

total_weighted_misfit = misfit_by_component.sum()
print("total weighted misfit", total_weighted_misfit)
