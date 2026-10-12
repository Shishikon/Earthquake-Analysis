import pandas as pd
from data_audit import dataset_summary, audit_columns
import matplotlib as plt
from pathlib import Path
import numpy as np



# Column droper
def drop_column(df, column):
    return df.drop(columns=[column])



# Load the dataset
LOCAL_FILE = Path("query.csv")
# FILE_URL = ("https://drive.google.com/file/d/1QRH4AMnR-uBIq5NsUk6DK5p2SIsb-QA3/view?usp=sharing")


raw = pd.read_csv(LOCAL_FILE)

copy = raw.copy()




# ////////////////// Working with columns start //////////////////

safe_test_columns = ['magType', 'nst', 'gap', 'dmin', 'rms', 'horizontalError', 'depthError', 'magError', 'magNst']



# =====COLUMN 'time' START=====
"""Create two columns, one for date another one for time, and drop original time column"""

# Convert time to datatime format
datatime_col = pd.to_datetime(copy['time'], errors='coerce')

# Creating new column date for dates
copy['date'] = datatime_col.dt.date

# Creating new column time for times
copy['time'] = datatime_col.dt.strftime('%H:%M:%S')

# Drop time column
copy = drop_column(copy, 'time')
# =====COLUMN 'time' END=====




# =====COLUMN 'depth' START=====

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

# Drop depth columns
copy = drop_column(copy, 'depth')
# =====COLUMN 'depth' END=====




# =====COLUMN 'net' START=====
copy['net'] = copy['net'].map({'us':'USGS',
                               'iscgem':'ISC-GEM',
                               'iscgemsup': 'ISC-GEM Supp'})
# =====COLUMN 'net' START=====



# =====COLUMN 'locationSource' START=====
copy = drop_column(copy, 'locationSource')
# =====COLUMN 'locationSource' END=====

# =====COLUMN 'magSource' START=====
copy = drop_column(copy, 'magSource')
# =====COLUMN 'magSource' END=====


# =====COLUMN 'id' START=====
copy = drop_column(copy, 'id')
# =====COLUMN 'id' END=====


# =====COLUMN 'updated' START=====
copy = drop_column(copy, 'updated')
# =====COLUMN 'updated' END=====





# =====COLUMN 'place' START=====
countries = ['Tajikistan', 'Uzbekistan', 'Turkmenistan', 'Kazakhstan', 'Kyrgyzstan', 'Iran', 'Afghanistan']

def find_country(text):
    found = [c for c in countries if c in text]
    if len(found) == 1:
        return found[0]
    if len(found) > 1:
        return 'Border region'
    return 'Unknown'

copy['country'] = copy['place'].apply(find_country)
copy['nearest location'] = copy['place'].str.rsplit(",", n=1).str[0].str.strip()

# drop place column
copy = drop_column(copy, 'place')
# =====COLUMN 'place' END=====


# =====COLUMN 'type' START=====
copy = drop_column(copy, 'type')
# =====COLUMN 'type' END=====


# =====COLUMN 'status' START=====
copy = drop_column(copy, 'status')
# =====COLUMN 'status' END=====




# ////////////////// Working with columns end //////////////////












audit = pd.DataFrame({
    "dtype": copy.dtypes.astype(str),
    "unique values": copy.nunique(dropna=False),
    "missing values": copy.isna().sum(),
    "duplicated values": copy.duplicated().sum(),
})


audit_columns = audit_columns(copy)
dataset_summary = dataset_summary(copy)
print(audit_columns)


# Datatype check
column_types = copy.dtypes


# 2 Strip all whitespace in object and str columns
for col in copy.select_dtypes(["object", "str"]).columns:
    copy[col] = copy[col].astype(str).str.strip()


# 3 Check for duplicates
duplicates = copy.duplicated().sum()


# 4 Check missing vals
missing_values = copy.isna().sum()



# 5 See unique values of columns where sum is less than 10
for i in copy.columns:
    if copy[i].nunique(dropna=False) < 10:
        uniq_vals = i
        uniq_vals_num = copy[i].nunique(dropna=False)
        uniq_vals_list = copy[i].unique().tolist()

        uniq_list = uniq_vals, uniq_vals_num, uniq_vals_list

# 6 Limit float columns up to 3 digits
for col in copy.select_dtypes('float').columns:
    copy[col] = copy[col].round(3)










"""
                       time  latitude  longitude  depth  mag magType   nst    gap  dmin   rms net          id                   updated                          place        type  horizontalError  depthError  magError  magNst    status locationSource magSource
0  2026-09-09T20:17:10.315Z   38.8791    70.5965   10.0  4.6      mb  27.0  144.0  1.11  0.68  us  us7000tg5i  2026-10-02T18:18:57.040Z  25 km SE of Rasht, Tajikistan  earthquake             5.33       1.893     0.116    22.0  reviewed             us        us


"""






