
import pandas as pd
from config import *

class LagsRollingAverageDiffsEWMsFeaturesGenerator:
    def __init__(self, df_sales: pd.DataFrame, store_name: str, sku_name: str, sales_name: str, date_name: str, end_date: str,
                 start_date_of_test: str, lags_back: list, windows: list, diff_lags: list, ewms: list):
        self.df_sales = df_sales
        self.store_name = store_name
        self.sku_name = sku_name
        self.sales_name = sales_name
        self.date_name = date_name
        self.end_date = end_date
        self.start_date_of_test = start_date_of_test
        self.lags_back = lags_back
        self.windows = windows
        self.diff_lags = diff_lags
        self.ewms = ewms


    def sum_agg_per_sku_date_store(self, data):
        data = data.groupby([self.date_name, self.store_name, self.sku_name]).sum()[self.sales_name].reset_index()
        data[self.sku_name] = data[self.sku_name].astype('category')
        data[self.store_name] = data[self.store_name].astype('category')
        return data

    def add_sku_store_id_col(self, df):
        ''' Add a column with the sku and store id.

            Args:
                    df: The dataframe to add the column to.
                    DEFAULT_SKU_NAME: The default name of the sku column.
                    DEFAULT_STORE_NAME: The default name of the store column.

            Returns:
                    The dataframe with the new column.

            '''
        df['sku, store'] = list(zip(df[self.sku_name], df[self.store_name]))
        return df

    def take_more_then_0_sales_and_set_index_to_date(self, data):
        ''' Take only the rows with more then 0 sales and set the index to the date.

            Args:
                    data: The dataframe to take the rows from.
                    DEFAULT_DATE_NAME: The default name of the date column.
                    DEFAULT_SALES_NAME: The default name of the sales column.

            Returns:
                    The dataframe with the new index.

            '''
        data = data[data[self.sales_name] > 0]
        data = data.set_index(self.date_name)
        data.index = pd.to_datetime(data.index)
        return data

    def add_lags_and_rolling_averages_and_diffs_and_ewms(self, df1, item):
        for lag in self.lags_back:
            df1[f'{item}_sales_lag_{lag}'] = df1['sales'].shift(lag)
        for window in self.windows:
            df1[f'{item}_sales_rolling_{window}'] = df1['sales'].shift(1).rolling(window).mean()
        for diff_lag in self.diff_lags:
            df1[f'{item}_sales_diff_{diff_lag}'] = df1['sales'].shift(1) - df1['sales'].shift(diff_lag)
        for ewm in self.ewms:
            df1[f'{item}_sales_ewm_{ewm}'] = df1['sales'].shift(1).ewm(alpha=ewm).mean()
        return df1

    def fill_0_in_gaps_sku_store_dates_until_end_date_df(self, df_of_sku_store_sales):
        df_of_sku_store_sales = df_of_sku_store_sales.reindex(pd.date_range(min(df_of_sku_store_sales.index), self.end_date))

        return df_of_sku_store_sales

    def return_df_of_sku_store_sales_with_lags_rolling_diff_ewm(self, data):
        df_of_sku_store_sales = pd.DataFrame()
        i = 0
        for sku_store in data["sku, store"].unique():
            i += 1
            sku_store_data = data[data["sku, store"] == sku_store]
            sku_store_data['sku, store'] = [sku_store] * len(sku_store_data)
            sku_store_data = LagsRollingAverageDiffsEWMsFeaturesGenerator.add_lags_and_rolling_averages_and_diffs_and_ewms(self, sku_store_data[['sales']], 'id')
            sku_store_data['sku, store'] = [sku_store] * len(sku_store_data)
            df_of_sku_store_sales = pd.concat([sku_store_data.reset_index().rename(columns={"index": "date"})])
        return df_of_sku_store_sales


    def return_df_of_store_sales_with_lags_rolling_diff_ewm(self, data):
        df_of_store_sales = pd.DataFrame()
        i = 0
        for store in data["store"].unique():
            i += 1
            store_data = data[data["store"] == store].groupby("date").sum()
            store_data['store'] = store
            store_data = LagsRollingAverageDiffsEWMsFeaturesGenerator.add_lags_and_rolling_averages_and_diffs_and_ewms(self, store_data[['sales']], self.store_name)
            store_data['store'] = store
            df_of_store_sales = pd.concat([store_data.reset_index().rename(columns={"index": "date"})])
        return df_of_store_sales

    def return_df_of_sku_sales_with_lags_rolling_diff_ewm(self, data):
        df_of_sku_sales = pd.DataFrame()
        i = 0
        for sku in data["sku"].unique():
            i += 1
            sku_data = data[data["sku"] == sku].groupby("date").sum()
            sku_data['sku'] = sku
            sku_data = LagsRollingAverageDiffsEWMsFeaturesGenerator.add_lags_and_rolling_averages_and_diffs_and_ewms(self, sku_data[['sales']], self.sku_name)
            sku_data['sku'] = sku
            df_of_sku_sales = pd.concat([sku_data.reset_index().rename(columns={"index": "date"})])

        return df_of_sku_sales