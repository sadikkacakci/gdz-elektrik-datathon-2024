import pandas as pd
import numpy as np
from datetime import datetime

class Preprocessor:
    def __init__(self, file_path,file_type):
        self.file_path = file_path
        self.df = pd.read_csv(self.file_path)
        self.file_type = file_type

    def split_il_ilce(self):
        self.df[['il', 'ilce']] = self.df['ilce'].str.split('-', expand=True)

    def convert_datetime_tarih(self):
        self.df["tarih"] = pd.to_datetime(self.df["tarih"])

    def convert_int_sums(self):
        if self.file_type == "train":
            self.df["bildirimsiz_sum"] = self.df["bildirimsiz_sum"].astype(int)
            self.df["bildirimli_sum"] = self.df["bildirimli_sum"].astype(int)
        else:
            self.df["bildirimli_sum"] = self.df["bildirimli_sum"].astype(int)

    def fill_nan_values(self,temp_df):
        temp_df["bildirimsiz_sum"] = temp_df["bildirimsiz_sum"].interpolate(method="linear")
        temp_df["bildirimli_sum"] = temp_df["bildirimli_sum"].interpolate(method="linear")
        return temp_df

    def fill_missing_dates(self, fill_nan=False):
        full_df = pd.DataFrame()
        cities = self.df["il"].unique()
        for city in cities:
            ilceler = self.df.loc[self.df["il"] == city]["ilce"].unique()
            for ilce in ilceler:
                temp = self.df.loc[(self.df["il"] == city) & (self.df["ilce"] == ilce)]
                min_date = temp['tarih'].min()
                max_date = datetime(2024, 1, 31)# datetime(2024, 1, 3)
                date_range = pd.date_range(start=min_date, end=max_date)
                missing_dates = date_range[~date_range.isin(temp['tarih'])]
                if len(missing_dates) == 0:
                    full_df = pd.concat([full_df, temp])
                    continue
                missing_df = pd.DataFrame({'tarih': missing_dates, 'ilce': ilce, 'il': city, 'bildirimsiz_sum': np.nan, 'bildirimli_sum': np.nan})
                ilce_full_df = pd.concat([temp, missing_df])
                if fill_nan and ilce_full_df.isna().sum().sum() > 0:
                    ilce_full_df = self.fill_nan_values(ilce_full_df)
                ilce_full_df = ilce_full_df.sort_values('tarih').reset_index(drop=True)
                full_df = pd.concat([full_df, ilce_full_df])
        full_df.reset_index(drop=True,inplace=True)
        self.df = full_df
        

    # def split_year_month_day(self):
    #     self.df['year'] = self.df['tarih'].dt.year
    #     self.df['month'] = self.df['tarih'].dt.month
    #     self.df['day'] = self.df['tarih'].dt.day
    #     self.df.drop("tarih", axis=1, inplace=True)

    def get_processed_df(self):
        if self.file_type == "train":
            fill_nan = True
        else:
            fill_nan = False
        self.split_il_ilce()
        self.convert_datetime_tarih()
        self.convert_int_sums()
        self.fill_missing_dates(fill_nan)
        return self.df
    