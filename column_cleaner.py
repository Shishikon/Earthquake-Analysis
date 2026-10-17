import pandas as pd

class EarthquakeDataCleaner:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.countries = [
            'Tajikistan', 'Uzbekistan', 'Turkmenistan',
            'Kazakhstan', 'Kyrgyzstan', 'Iran', 'Afghanistan'
        ]

    def drop_columns(self, columns: list):
        cols_to_drop = [col for col in columns if col in self.df.columns]
        self.df = self.df.drop(columns=cols_to_drop)
        return self


    def clean_time(self):
        datetime_col = pd.to_datetime(self.df['time'], errors='coerce', utc=True)
        self.df['date'] = datetime_col.dt.date
        self.df['time_only'] = datetime_col.dt.strftime('%H:%M:%S')
        return self.drop_columns(['time'])


    def clean_depth(self):
        self.df['depth_class'] = pd.cut(
            self.df['depth'],
            bins=[-float('inf'), 10, 35, 70, 100, 150, 300],
            labels=[
                'very_shallow', 'shallow', 'moderately_shallow',
                'intermediate_1', 'intermediate_2', 'intermediate_3'
            ]
        )
        return self.drop_columns(['depth'])


    def clean_net(self):
        self.df['net'] = self.df['net'].map({
            'us': 'USGS',
            'iscgem': 'ISC-GEM',
            'iscgemsup': 'ISC-GEM Supp'
        })
        return self


    def clean_place(self):
        def find_country(text):
            found = [c for c in self.countries if c in str(text)]
            if len(found) == 1:
                return found[0]
            if len(found) > 1:
                return 'Border region'
            return 'Unknown'

        self.df['country'] = self.df['place'].apply(find_country)
        self.df['nearest location'] = self.df['place'].str.rsplit(",", n=1).str[0].str.strip()
        return self.drop_columns(['place'])


    def post_process(self):
        # Strip whitespace from object/str columns
        for col in self.df.select_dtypes(["object", "str"]).columns:
            self.df[col] = self.df[col].astype(str).str.strip()

        # Limit float columns up to 3 digits
        for col in self.df.select_dtypes('float').columns:
            self.df[col] = self.df[col].round(3)
        return self


    def run_pipeline(self):
        """Executes the complete data transformation pipeline in order."""
        (self.clean_time()
             .clean_depth()
             .clean_net()
             .clean_place()
             .drop_columns(['id', 'updated', 'type', 'locationSource', 'magSource', 'status'])
             .post_process())
        return self.df