import pandas as pd
from data_audit import dataset_summary, audit_columns
import matplotlib as plt
from pathlib import Path
import numpy as np
from column_cleaner import *



# Load the dataset
LOCAL_FILE = Path("Files/query.csv")
# FILE_URL = ("https://drive.google.com/file/d/1QRH4AMnR-uBIq5NsUk6DK5p2SIsb-QA3/view?usp=sharing")


raw = pd.read_csv(LOCAL_FILE)

copy = raw.copy()





# ////////////////// Working with columns start //////////////////

safe_test_columns = ['magType', 'nst', 'gap', 'dmin', 'rms', 'horizontalError', 'depthError', 'magError', 'magNst']


# =====COLUMN 'time' START=====
copy = time_col(copy)
# =====COLUMN 'time' END=====




# =====COLUMN 'depth' START=====
copy = depth_col(copy)
print(copy['depth_class'].value_counts())
# =====COLUMN 'depth' END=====




# =====COLUMN 'net' START=====
copy['net'] = copy['net'].map({'us':'USGS',
                               'iscgem':'ISC-GEM',
                               'iscgemsup': 'ISC-GEM Supp'})
# =====COLUMN 'net' END=====


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


# =====COLUMN 'locationSource' START=====
copy = drop_column(copy, 'locationSource')
# =====COLUMN 'locationSource' END=====

# =====COLUMN 'magSource' START=====
copy = drop_column(copy, 'magSource')
# =====COLUMN 'magSource' END=====




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











