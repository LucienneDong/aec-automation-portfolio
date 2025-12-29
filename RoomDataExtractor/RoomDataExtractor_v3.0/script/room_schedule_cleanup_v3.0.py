python
import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename
Tk().withdraw()

# Let the user to select a csv file for data
input_path = askopenfilename(
  title="Select Room Schedule CSV",
  filetypes=[("CSV files", "*.csv"),("All files", "*.*")]
)
print("You selected: ", input_path)

# Read selected csv file, and skip the junk data
df = pd.read_csv(input_path, on_bad_lines='skip')

# Data Validation
## Let the user check the last 5 rows of the file
print("Please check the last 5 rows of the data")
print(df.head())

## Let the user confirm all info are included. Otherwise do exit
print("Columns in the CSV:")
print(df.columns)

## Ask the user to confirm if all info from revit is included, if not stop the script
root = Tk()
root.withdraw()

from tkinter import Tk, messagebox

confirm = messagebox.askyesno(
  "Confirm Columns",
  "Are all required columns from the Revit Room Schedule included?"
)
if not confirm:
  messagebox.showinfo("Exit", "Please check the CSV file. Exiting script.")
  root.destroy()
  exit()

## Flag bad rooms. Output error list
### Missing data
df_missing_data = df[df.isna().any(axis=1)]
### Let the user check the results
print(df_missing_data.head())

## Detect invalid placeholder text.
### Data with 'Not Placed'
not_placed_row = df[df.isin(['Not Placed']).any(axis=1)]
print(not_placed_row)
### Data with 'Redundant Room'
redundant_room_row = df[df.isin(['Redundant Room']).any(axis=1)]
print(redundant_room_row)
### Data with 'Unassigned'
unassigned_row = df[df.isin(['Unassigned']).any(axis=1)]
print(unassigned_row)
### Data with 'N/A'
NA_row = df[df.isin(['N/A']).any(axis=1)]
print(NA_row)

## Data type validation (str vs int)
### Convert area into numeric
df['Area_num'] = pd.to_numeric(df["Area (SF)"], errors="coerce")
### Filter the invalid rows
invalid_area_row = df[df['Area_num'].isna()]
### Print invalid rows under Area (SF)
print(invalid_area_row)

## Update Data type validation on level numbers
## Cleanup the prefix in the level number before validation
df["Level"] = (
    df["Level"]
    .astype(str)
    .str.replace(r"^\s*\d{2,3}-\d\s*-\s*","", regex=True)
    .str.replace(r"^-Level", "Level", regex=True)
    .str.strip()
)

## Extract only the integar after 'Level'
df["Level_num"] = df["Level"].str.extract(r"Level\s*(\d+)", expand=False)
df['Level_num'] = pd.to_numeric(df["Level_num"], errors = "coerce")
invalid_level_row = df[df['Level_num'].isna()]
print(invalid_level_row)

## Numeric range check
### Check numbers <0 or unrealistic high
level_min = 0
level_max = 20

area_min = 1
area_max = 5000

df_invalid_area_range = df[
(df['Area_num']< area_min) |
(df['Area_num']> area_max)
]
print(df_invalid_area_range)

df_invalid_level_range = df[
(df['Level_num']< level_min) |
(df['Level_num']> level_max)
]
print(df_invalid_level_range)

### Count violations
print(f"invalid Area rows: {len(df_invalid_area_range)}")
print(f"invalid Level rows: {len(df_invalid_level_range)}")

## Duplicate data detection
### Duplicate room numbers
dup_room_number = df[df.duplicated(subset=['Number'], keep=False)]
print("Duplicate Room Number Found:")
print(dup_room_number[['Level','Number', 'Name']].head())
print(f"\nTotal duplicate room number rows: {len(dup_room_number)}")

### Duplicate room number + level combo
dup_room_level = df[df.duplicated(subset=['Number','Level'], keep=False)]
print("Duplicate Room Number Found:")
print(dup_room_level[['Level','Number', 'Name']].head())
print(f"\nTotal duplicate room+level rows: {len(dup_room_level)}")

# Create issue repo
## Skip empty lists
def label_issue(df,label):
    if df.empty:
        return df
    df = df.copy()
    df.loc[df.index,"issue_type"] = label
    return df

## Assign labels to lists
df_missing_data = label_issue(df_missing_data, "Missing Data")
not_placed_row = label_issue(not_placed_row, "Not Placed")
redundant_room_row = label_issue(redundant_room_row, "Redundant Room")
unassigned_row = label_issue(unassigned_row, "Unassigned")
NA_row = label_issue(NA_row, "N/A Found")
invalid_area_row = label_issue(invalid_area_row, "Invalid Area Format")
invalid_level_row = label_issue(invalid_level_row, "Invalid Level Format")
df_invalid_area_range = label_issue(df_invalid_area_range, "Area Out of Range")
df_invalid_level_range = label_issue(df_invalid_level_range, "Level Out of Range")
dup_room_number = label_issue(dup_room_number, "Duplicate Room Number")
dup_room_level = label_issue(dup_room_level, "Duplicate Room+Level")

issue_report = pd.concat([
    df_missing_data,
    not_placed_row,
    redundant_room_row,
    unassigned_row,
    NA_row,
    invalid_area_row,
    invalid_level_row,
    df_invalid_area_range,
    df_invalid_level_range,
    dup_room_number,
    dup_room_level
], ignore_index=True)

## Consolidate the issue repo
### Group by the room identifiers and merge all issue types into one cell
df_issues = (
    issue_report
    .groupby(["Level","Number","Name"], dropna=False)["issue_type"]
    .apply(lambda x: ";".join(sorted(set(x.astype(str)))))
    .reset_index()
)

### Rename the merged issue column so it’s clear in the report
df_issues = df_issues.rename(columns={"issue_type": "all_issues"})

# Report issue for user to check
## Export the csv file to user's selected location
from tkinter.filedialog import asksaveasfilename
output_path = asksaveasfilename(
    title="Save Missing Data Room Schedule",
    defaultextension=".csv",
    filetypes=[("CSV files","*.csv")]
    )
print("File will be saved to: ",output_path)

df_issues.to_csv(output_path, index=False)
