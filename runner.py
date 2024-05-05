import pandas as pd
from preprocessor import Preprocessor
from weather import Weather
from data_holidays import Holidays
import warnings
warnings.filterwarnings("ignore")


def merge_weather_holiday(main_df, weather_df, holidays_list):
    merged_df = pd.merge(main_df, weather_df, on=["tarih","il","ilce"])
    merged_df["is_holiday"] = 0
    merged_df.loc[merged_df['tarih'].isin(holidays_list),"is_holiday"] = 1
    return merged_df

def split_year_month_day(df):
    # Yıl, ay ve gün sütunlarını oluşturun.
    df['year'] = df['tarih'].dt.year
    df['month'] = df['tarih'].dt.month
    df['day'] = df['tarih'].dt.day
    df.drop("tarih",axis = 1,inplace = True)
    return df
    
def runner(train_path,test_path,weather_path,holidays_path,split_year_month_bool=True):
    # train_path = "data/train.csv"
    preprocessor = Preprocessor(train_path,"train")
    train_df = preprocessor.get_processed_df()

    # test_path = "data/test.csv"
    preprocessor = Preprocessor(test_path,"test")
    test_df = preprocessor.get_processed_df()

    # weather_path = "data/weather.csv"
    set_daily_data_bool = True
    normalize_weather_data_daily_bool = True
    weather_class = Weather(weather_path,set_daily_data_bool,normalize_weather_data_daily_bool)
    weather_data_daily_normalized = weather_class.get_weather_data_daily_normalized()

    # holidays_path = "data/holidays.csv"
    holiday_class = Holidays(holidays_path)
    holidays_list = holiday_class.get_holidays()

    train_df = merge_weather_holiday(train_df,weather_data_daily_normalized,holidays_list)
    test_df = merge_weather_holiday(test_df,weather_data_daily_normalized,holidays_list)

    if split_year_month_bool:
        train_df = split_year_month_day(train_df)
        test_df = split_year_month_day(test_df)

    return train_df,test_df