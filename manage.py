import pandas as pd
from data_audit import dataset_summary, audit_columns
import matplotlib as plt
from pathlib import Path
import numpy as np



# Column droper
def drop_column(df, column):
    return df.drop(columns=[column])



# Load the dataset
LOCAL_FILE = Path("Files/query.csv")
FILE_URL = ("https://drive.google.com/file/d/1QRH4AMnR-uBIq5NsUk6DK5p2SIsb-QA3/view?usp=sharing")

if LOCAL_FILE.exists():
    raw = pd.read_csv(LOCAL_FILE)
else:
    raw = pd.read_csv(FILE_URL)

copy = raw.copy()




audit = pd.DataFrame({
    "dtype": copy.dtypes.astype(str),
    "unique values": copy.nunique(dropna=False),
    "missing values": copy.isna().sum(),
    "duplicated values": copy.duplicated().sum(),
})

audit_columns = audit_columns(copy)


# Datatype check
column_types = copy.dtypes









# ////////////////// Working with columns start //////////////////


# -----COLUMN 'time' START-----
"""Create two columns, one for date another one for time, and drop original time column"""

# Convert time to datatime format
datatime_col = pd.to_datetime(copy['time'], errors='coerce')

# Creating new column date for dates
copy['Date'] = datatime_col.dt.date

# Creating new column time for times
copy['Time'] = datatime_col.dt.strftime('%H:%M:%S')

# Drop time column
copy = drop_column(copy, 'time')
# -----COLUMN 'time' END-----



# -----COLUMN 'depth' START-----

copy['depth_class'] = pd.cut(
    copy['depth'],
    bins=[-float('inf'), 10, 35, 70, 100, 150, 300],
    labels=[
        'very_shallow',
        'shallow',
        'moderately_shallow',
        'intermediate_1',
        'intermediate_2',
        'intermediate_3'
    ]
)
print(copy.columns)
# -----COLUMN 'depth' END-----





# -----COLUMN 'mag' START-----



# print(copy['mag'])
# -----COLUMN 'mag' END-----






# ////////////////// Working with columns end //////////////////






















# 2 Strip all whitespace in object and str columns
for col in copy.select_dtypes(["object", "str"]).columns:
    copy[col] = copy[col].astype(str).str.strip()
"""All object types were striped"""

# 3 Check for duplicates
duplicates = copy.duplicated().sum()
"""Returned 0 duplicated values"""

# 4 Check missing vals
missing_values = copy.isna().sum()
"""
Missing values 
nst                821
gap                682
dmin               930
rms                267
horizontalError    950
depthError         694
magError           854
magNst             307
REST               0
"""


# 4.1 ID duplication
ids = copy['id'].duplicated().sum()
"""0"""


# 5 See unique values of columns where sum is less than 10
for i in copy.columns:
    if copy[i].nunique(dropna=False) < 10:
        uniq_vals = i
        uniq_vals_num = copy[i].nunique(dropna=False)
        uniq_vals_list = copy[i].unique().tolist()

        uniq_list = uniq_vals, uniq_vals_num, uniq_vals_list

        """
        1) 'status' has one unique value for all rows.
        2) 'type' has 2 unique values, earthquake and nuclear explosions
        Nuclear explosions has 2 rows, so i will drop rows with nuclear explosions.
        3) Both columns has 1 unique values so i drop both status and type columns.
        """


# 6 Limit float columns up to 3 digits
for col in copy.select_dtypes('float').columns:
    copy[col] = copy[col].round(3)










"""
                       time  latitude  longitude  depth  mag magType   nst    gap  dmin   rms net          id                   updated                          place        type  horizontalError  depthError  magError  magNst    status locationSource magSource
0  2026-09-09T20:17:10.315Z   38.8791    70.5965   10.0  4.6      mb  27.0  144.0  1.11  0.68  us  us7000tg5i  2026-10-02T18:18:57.040Z  25 km SE of Rasht, Tajikistan  earthquake             5.33       1.893     0.116    22.0  reviewed             us        us


"""






