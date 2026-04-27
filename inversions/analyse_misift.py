import pandas as pd
import argparse

parser = argparse.ArgumentParser(
    description="Compute weighted misfit from a misfit file."
)
parser.add_argument("filename", type=str, help="Path to the misfit file")

args = parser.parse_args()
filename = args.filename


df = pd.read_csv(args.filename, sep="\s+")
#pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)
#print(df)


# Check the first few rows
print(df.head())

# Group by 'component' and compute sum(weight * misfit)
df["weighted_misfit"] = df["weight"] * df["misfit"]
misfit_by_component = df.groupby("component")["weighted_misfit"].sum()



# Print the result
print(misfit_by_component)

# Assuming 's' is your Series
strong = misfit_by_component[['HNE', 'HNN', 'HNZ']].sum()
body = misfit_by_component[['P', 'SH']].sum()
gnss = misfit_by_component['GNSS']
surface = misfit_by_component[['R', 'SH']].sum()

print("strong body gnss surface")
print(strong, body, gnss, surface)

count_weight = df.groupby("component")["weight"].sum()
print(count_weight)


total_weighted_misfit = misfit_by_component.sum()
print("total weighted misfit", total_weighted_misfit)
