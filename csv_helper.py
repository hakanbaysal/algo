from datetime import timedelta
import pandas as pd


# CSV Helper class
class CSVHelper:

    def __init__(self):
        pass

    # read csv file
    def read_csv(self, csv_file: str):
        df = pd.read_csv(csv_file)
        return df

    # get data from csv file between two dates
    def date_filter(self, df: pd, min_date: str, max_date: str):
        min_date = pd.to_datetime(min_date)
        min_date = min_date.strftime("%Y-%m-%d")
        max_date = pd.to_datetime(max_date)
        max_date = max_date.strftime("%Y-%m-%d")

        df = df.loc[(df['date'] <= max_date) & (df['date'] >= min_date)]
        return df

    # find datas by queries
    def query(self, df: pd, queries: list):
        for query in queries:
            if type(query['value']) is not list:
                query['value'] = [query['value']]
            df = df.loc[df[query['field']].isin(query['value'])]
        return df

    # calculate MA7
    def MA7(self, df: pd, date: str, queries: list):
        min_date = pd.to_datetime(date) - timedelta(days=7)
        min_date = min_date.strftime("%Y-%m-%d")
        max_date = pd.to_datetime(date) - timedelta(days=1)
        max_date = max_date.strftime("%Y-%m-%d")

        df = df.loc[(df['date'] <= max_date) & (df['date'] >= min_date)]
        df = self.query(df, queries)
        return self.float_eight_digits(df['quantity'].sum() / 7)

    # calculate LAG7
    def LAG7(self, df: pd, date: str, queries: list):
        min_date = pd.to_datetime(date) - timedelta(days=7)
        min_date = min_date.strftime("%Y-%m-%d")

        df = df.loc[(df['date'] == min_date)]
        df = self.query(df, queries)
        return self.float_eight_digits(df['quantity'].sum())

    # float to 8 digits
    def float_eight_digits(self, number: float):
        return round(number, 8)

    # calculate WMAPE (Weighted Mean Absolute Percentage Error)
    def wmape_process(self, wmape: pd, top: int):
        df = pd.DataFrame(wmape, columns=['product', 'store', 'brand', 'actual', 'forecast'])
        wmape_series = df.groupby(['product', 'store', 'brand']).apply(
            lambda x: sum(abs(x['actual'] - x['forecast'])) / sum(abs(x['actual'])))
        wmape_df = pd.DataFrame(wmape_series, columns=['WMAPE'])
        return wmape_df.sort_values("WMAPE", ascending=False).head(top)

    # create feature.csv file
    def write_features_csv(self, series: list, csv_file: str):
        df = pd.DataFrame(series,
                          columns=['product_id', 'store_id', 'brand_id', 'date', 'sales_product', 'MA7_P', 'LAG7_P',
                                   'sales_brand', 'MA7_B', 'LAG7_B', 'sales_store', 'MA7_S', 'LAG7_S'])
        df.to_csv(csv_file, index=True)

    # create mapes.csv file
    def write_mapes_csv(self, wmape_df: pd, csv_file: str):
        series = []
        for index, row in wmape_df.iterrows():
            product = int(index[0])
            store = int(index[1])
            brand = int(index[2])
            wmape_val = self.float_eight_digits(row.values[0])
            series.append([product, store, brand, wmape_val])
        df = pd.DataFrame(series, columns=['product_id', 'store_id', 'brand_id', 'WMAPE'])
        df.to_csv(csv_file, index=True)
