import pandas as pd

class Holidays:
    def __init__(self, holidays_path):
        self.holidays_path = holidays_path

    def get_holidays(self):
        # Tatil verilerini yükle
        holidays_df = pd.read_csv(self.holidays_path)

        # Yıl, Ay ve Gün sütunlarını birleştirerek tarih sütunu oluştur
        holidays_df['date'] = holidays_df['Yıl'].astype(str) + '-' + holidays_df['Ay'].astype(str) + '-' + holidays_df['Gün'].astype(str)
        holidays_df["date"] = pd.to_datetime(holidays_df["date"])

        # Tarih listesi olarak döndür
        return holidays_df["date"].tolist()