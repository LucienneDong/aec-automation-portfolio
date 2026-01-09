python
import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename
Tk().withdraw()

# Let the user to select a csv file for data clean
input_path = askopenfilename(
  title="Select Room Schedule CSV",
  filetypes=[("CSV files", "*.csv"),("All files", "*.*")]
)
print("You selected: ", input_path)

# Read selected csv file, and skip the junk data
df = pd.read_csv(input_path, on_bad_lines='skip')

# Let the user check the last 5 rows of the file
print("Please check the last 5 rows of the data")
print(df.head())

# Let the user confirm all info are included. otherwise do exit
print("Columns in the CSV:")
print(df.columns)

# Ask the user to confirm if all info from revit is included
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

# Detect and show the data with 'Not Placed'
not_placed_row = df[df.isin(['Not Placed']).any(axis=1)]
print(not_placed_row)

# Cleanup 'Not Placed' rows
df = df[~df.isin(['Not Placed']).any(axis=1)]

# Cleanup redundant room
df = df[df['Area (SF)']!='Redundant Room']

# Cleanup Level data. keep rows with "Level x" and cleanup the data. omit the other ones
df["level_num"] = (
  df["Level"]
  .astype(str)
  .str.extract(r"Level\s*(\d+)",expand=False)
)
df["level_num"] = pd.to_numeric(df["level_num"], errors="coerce")
df = df.dropna(subset=["level_num"])
df["level_num"] = df["level_num"].astype(int)

# Export the cleaned up csv file to user's selected location
from tkinter.filedialog import asksaveasfilename
output_path = asksaveasfilename(
    title="Save Cleaned Room Schedule",
    defaultextension=".csv",
    filetypes=[("CSV files","*.csv")]
    )
print("File will be saved to: ",output_path)

df.to_csv(output_path, index=False)
