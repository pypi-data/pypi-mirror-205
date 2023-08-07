import numpy as np
import pandas as pd

from .. import config as global_config
from . import config as config

store_col_str = global_config.STORE_COLUMN_NAME
sku_col_str = global_config.SKU_COLUMN_NAME
date_col_str = global_config.DATE_COLUMN_NAME
sales_col_str = global_config.SALES_COLUMN_NAME
id_col_str = global_config.ID_COLUMN_NAME
sku_store_col_str = global_config.SKU_STORE_COLUMN_NAME

class LagFeatureGenerator:
    def __init__(self, daily_lags_back=config.DAILY_LAGS_BACK,
                 daily_windows=config.DAILY_WINDOWS,
                 daily_diff_lags=config.DAILY_DIFF_LAGS,
                 daily_ewms=config.DAILY_EWMS):
        self.daily_lags_back = daily_lags_back
        self.daily_windows = daily_windows
        self.daily_diff_lags = daily_diff_lags
        self.daily_ewms = daily_ewms

    def add_lags_and_rolling_averages_and_diffs_and_ewms(self, df, base_column_name):
        for lag in self.daily_lags_back:
            df[f'{base_column_name}_sales_lag_{lag}'] = df[sales_col_str].shift(lag)
        for window in self.daily_windows:
            df[f'{base_column_name}_sales_rolling_{window}'] = df[sales_col_str].shift(1).rolling(window).mean()
        for diff_lag in self.daily_diff_lags:
            df[f'{base_column_name}_sales_diff_{diff_lag}'] = df[sales_col_str].shift(1) - df[sales_col_str].shift(diff_lag)
        for ewm in self.daily_ewms:
            df[f'{base_column_name}_sales_ewm_{ewm}'] = df[sales_col_str].shift(1).ewm(alpha=ewm).mean()
        return df



class StoreLagFeatureGenerator(LagFeatureGenerator):
    def __init__(self):
        super().__init__()

    def create_all_stores_lags(self, store_data_df, predict_date):
        """
        This function assumes that store_data_df is (regular_data_df ) filtered to include only rows from a specific store
        """
        store_df = store_data_df.groupby(date_col_str).sum().reset_index()[[date_col_str, sales_col_str]]
        store_df = store_df.set_index(date_col_str)

        store_df = self.add_lags_and_rolling_averages_and_diffs_and_ewms(df=store_df[[sales_col_str]], base_column_name=store_col_str)


        store_df = store_df.drop(columns=[sales_col_str]).reset_index()
        store_df = store_df[store_df[date_col_str] == pd.to_datetime(predict_date)]

        return store_df


class SKULagFeatureGenerator(LagFeatureGenerator):
    def __init__(self):
        super().__init__()

    def create_all_sku_lags(self, regular_data_df, predict_date):
        """
            This function assumes that regular_data_df is not filtered and accept include only rows from a specific sku
        """
        all_sku_lags = pd.DataFrame()
        for sku in regular_data_df[sku_col_str].unique():
            sku_data = regular_data_df[regular_data_df[sku_col_str] == sku].groupby(date_col_str).sum().reset_index()[
                [date_col_str, sales_col_str]]
            sku_data = sku_data.set_index(date_col_str)

            sku_data = self.add_lags_and_rolling_averages_and_diffs_and_ewms(sku_data[[sales_col_str]], sku_col_str)

            sku_data = sku_data.drop(columns=[sales_col_str]).reset_index()
            sku_data[sku_col_str] = np.int64(sku)

            all_sku_lags = pd.concat([all_sku_lags, sku_data], ignore_index=True)

        all_sku_lags = all_sku_lags[all_sku_lags[date_col_str] == pd.to_datetime(predict_date)]
        return all_sku_lags

class IDLagFeatureGenerator(LagFeatureGenerator):
    def __init__(self):
        super().__init__()

    def create_id_lags(self, id_data_df, sku, store, predict_date):

        id_data_df = self.add_lags_and_rolling_averages_and_diffs_and_ewms(id_data_df.set_index(date_col_str)[[sales_col_str]], id_col_str).reset_index()

        id_data_df[sku_col_str] = np.int64(sku)
        id_data_df[store_col_str] = np.int32(store)
        #id_data_df = id_data_df.drop(columns=[sku_store_col_str])
        id_data_df = id_data_df[id_data_df[date_col_str] == pd.to_datetime(predict_date)]
        return id_data_df


