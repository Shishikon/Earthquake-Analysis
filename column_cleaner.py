import pandas as pd

original_columns = ['latitude', 'longitude',
                    'mag', 'magType', 'nst',
                    'gap', 'dmin', 'rms', 'net', 'id',
                    'updated', 'place', 'type', 'horizontalError',
                    'depthError', 'magError', 'magNst',
                    'status','locationSource', 'magSource']
 # Column Droper
def drop_column(df, column):
    return df.drop(columns=[column])


# time
def time_col(df):
    datetime_col = pd.to_datetime(df['time'], errors='coerce', utc=True)

    df['date'] = datetime_col.dt.date
    df['time_only'] = datetime_col.dt.strftime('%H:%M:%S')

    df = drop_column(df, 'time')
    return df

# depth
def depth_col(df):
    df['depth_class'] = pd.cut(
        df['depth'],
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
    df = drop_column(df, 'depth')
    return df
