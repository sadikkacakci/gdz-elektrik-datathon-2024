import pandas as pd
from sklearn.preprocessing import MinMaxScaler

class Weather:
    def __init__(self, weather_path,set_daily_data_bool,normalize_weather_data_daily_bool):
        self.weather_path = weather_path
        self.weather_data = pd.read_csv(self.weather_path)
        self.weather_data.columns = self.weather_data.columns.str.replace('name', 'ilce')
        self.weather_data['ilce'] = self.weather_data['ilce'].str.lower()
        self.weather_data_daily = None
        self.weather_data_daily_normalized = None
        self.set_daily_data_bool = set_daily_data_bool
        self.normalize_weather_data_daily_bool = normalize_weather_data_daily_bool

    def set_daily_data(self):
        daily_df = pd.DataFrame()
        for ilce in self.weather_data["ilce"].unique():
            temp = self.weather_data.loc[self.weather_data["ilce"] == ilce]
            temp['date'] = pd.to_datetime(temp['date'])
            temp.set_index('date', inplace=True)

            # Günlük verileri toplula
            temp_daily_df = temp.resample('D').agg({
                't_2m:C': 'mean',  # Ortalama sıcaklık
                'effective_cloud_cover:p': 'mean',  # Ortalama bulutluluk
                'global_rad:W': 'mean',  # Ortalama güneşlilik değeri
                'relative_humidity_2m:p': 'mean',  # Ortalama bağıl nem
                'wind_dir_10m:d': 'mean',  # Ortalama rüzgar yönü
                'wind_speed_10m:ms': 'mean',  # Ortalama rüzgar hızı
                'prob_precip_1h:p': 'mean',  # Ortalama yağış olasılığı
                't_apparent:C': 'mean'  # Ortalama hissedilen sıcaklık
            })

            temp_daily_df["ilce"] = ilce
            daily_df = pd.concat([daily_df, temp_daily_df])

        self.weather_data_daily = daily_df.reset_index()

    def normalize_weather_data_daily(self):
        data = self.weather_data_daily.drop(["date", "ilce"], axis=1)

        # Verileri ölçeklendir
        scaler = MinMaxScaler()
        df_normalized = pd.DataFrame(scaler.fit_transform(data), columns=data.columns)
        daily_df_normalized = pd.concat([self.weather_data_daily[["date", "ilce"]], df_normalized], axis=1)

        # 'il' ve 'ilce'yi ayır
        daily_df_normalized[['il', 'ilce']] = daily_df_normalized['ilce'].str.split('-', expand=True)
        self.weather_data_daily_normalized = daily_df_normalized.rename(columns={'date': 'tarih'})

    def get_weather_data_daily_normalized(self):
        if self.set_daily_data_bool:
            self.set_daily_data()
        if self.normalize_weather_data_daily_bool:
            self.normalize_weather_data_daily()
        return self.weather_data_daily_normalized