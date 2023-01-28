import argparse
import numpy as np

from csv_helper import CSVHelper


# Create feature.csv and mapes.csv
# - "--min-date": start of the date range. type:str, format:"YYYY-MM-DD", default:"2021-01-08"
# - "--max-date": end of the date range. type:str, format:"YYYY-MM-DD", default:"2021-05-30"
# - "--top": number of rows in the WMAPE output. type:int, default:5
class Solution:

    # init method or constructor
    def __init__(self, min_date: str, max_date: str, top: int):
        self.min_date = min_date
        self.max_date = max_date
        self.top = top

        self.csv = CSVHelper()
        self.brand = self.csv.read_csv('data/brand.csv')
        self.product = self.csv.read_csv('data/product.csv')
        self.store = self.csv.read_csv('data/store.csv')
        self.sales = self.csv.read_csv('data/sales.csv')

        print("Started")
        self.features = []
        self.wmape = []
        self.feature()
        self.write_csv()
        print("Finished")

    # Calculate feature values
    def feature(self):
        # get sales data
        sales = self.csv.date_filter(self.sales, min_date, max_date)
        # loop sales data
        for index, row in sales.iterrows():
            # get product
            product = self.csv.query(self.product, [{'field': 'id', 'value': row['product']}])
            product_brand_name = product['brand'].values[0]
            # get brand
            brand = self.csv.query(self.brand, [{'field': 'name', 'value': product_brand_name}])
            brand_id = brand['id'].values[0]

            # get same brand products
            product = self.csv.query(self.product, [{'field': 'brand', 'value': product_brand_name}])
            same_brands_product_ids = np.array(product['id']).tolist()

            date = row['date']
            store_id = row['store']
            product_id = row['product']

            # find sales product in same store, calculate MA7_P, LAG7_P
            predicate = [{'field': 'date', 'value': date},
                         {'field': 'store', 'value': store_id},
                         {'field': 'product', 'value': product_id}]
            sales_product = self.csv.query(self.sales, predicate)
            sales_product = sales_product['quantity'].values[0]
            predicate = [{'field': 'store', 'value': store_id}, {'field': 'product', 'value': product_id}]
            MA7_P = self.csv.MA7(self.sales, date, predicate)
            LAG7_P = self.csv.LAG7(self.sales, date, predicate)

            # find sales brand in same store, calculate MA7_B, LAG7_B
            predicate = [{'field': 'date', 'value': date}, {'field': 'store', 'value': store_id},
                         {'field': 'product', 'value': same_brands_product_ids}]
            sales_brand = self.csv.query(self.sales, predicate)
            sales_brand = sales_brand['quantity'].sum()
            predicate = [{'field': 'store', 'value': store_id}, {'field': 'product', 'value': same_brands_product_ids}]
            MA7_B = self.csv.MA7(self.sales, date, predicate)
            LAG7_B = self.csv.LAG7(self.sales, date, predicate)

            # find sales store in same store, calculate MA7_S, LAG7_S
            predicate = [{'field': 'date', 'value': date}, {'field': 'store', 'value': store_id}]
            sales_store = self.csv.query(self.sales, predicate)
            sales_store = sales_store['quantity'].sum()
            predicate = [{'field': 'store', 'value': store_id}]
            MA7_S = self.csv.MA7(self.sales, date, predicate)
            LAG7_S = self.csv.LAG7(self.sales, date, predicate)

            # add feature
            self.features.append(
                [row['product'], row['store'], brand_id, row['date'], sales_product, MA7_P, LAG7_P, sales_brand, MA7_B,
                 LAG7_B, sales_store, MA7_S, LAG7_S])
            # add wmape
            self.wmape.append([row['product'], row['store'], brand_id, sales_product, MA7_P])

    # create new dataframes and write to csv
    def write_csv(self):
        self.csv.write_features_csv(self.features, 'features.csv')
        print("features.csv is created")

        wmape_df = self.csv.wmape_process(self.wmape, top)
        self.csv.write_mapes_csv(wmape_df, 'mapes.csv')
        print("mapes.csv is created")


# main method
if __name__ == '__main__':
    # get arguments
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-min", "--min-date", help="minimum date", type=str, required=True, default="2021-01-08")
    argParser.add_argument("-max", "--max-date", help="maximum date", type=str, required=True, default="2021-05-30")
    argParser.add_argument("-top", "--top", help="top", type=int, required=True, default=5)
    args = argParser.parse_args()

    min_date = args.min_date
    max_date = args.max_date
    top = args.top
    # call Solution class
    solution = Solution(min_date, max_date, top)
