import numpy as np
from typing import List
import pandas as pd

from .. import config


class CumulativeFeatureGenerator:
    @classmethod
    def filter_data_by_date(cls, df: pd.DataFrame, date_col: str, start_date: str) -> pd.DataFrame:
        df = df[df[date_col] >= start_date]
        return df

    @classmethod
    def groupby_sum_sku_store(cls, df: pd.DataFrame, target_col: str, sku_store_col: List[str],
                              date_col: str) -> pd.DataFrame:

        df[target_col] = df[target_col].astype(np.float64)
        return df.groupby(sku_store_col + [date_col])[target_col].sum().reset_index()

    @classmethod
    def add_cumulative_sum_column_respect_time(cls, df: pd.DataFrame, target_col: str, sku_store_col: List[str],
                                               list_freq: List[str], date_col: str) -> pd.DataFrame:
        df[date_col] = pd.to_datetime(df[date_col])
        sku_store_col_name = '_'.join(sku_store_col)
        for freq in list_freq:
            df_grouped = df.groupby(sku_store_col + [pd.Grouper(key=date_col, freq=freq)])[target_col].sum().reset_index()

            df_grouped[f"sales_cumulative_{sku_store_col_name}_{freq}"] = df_grouped.groupby(sku_store_col)[
                target_col].apply(lambda x: np.cumsum(x.shift(1).fillna(0)))

            df = df.merge(df_grouped.drop(columns=[target_col]), on=sku_store_col + [date_col], how='left').fillna(0)
            df = df.drop_duplicates(subset=sku_store_col + [date_col], keep='last')
        return df

    @classmethod
    def add_expected_value_column_respect_time(cls, df: pd.DataFrame, target_col: str, sku_store_col: List[str],
                                               list_freq: List[str], date_col: str) -> pd.DataFrame:
        sku_store_col_name = '_'.join(sku_store_col)
        df_expected = pd.DataFrame()
        df[target_col] = df[target_col].astype(np.float32)
        for freq in list_freq:
            df_temp = df.groupby(sku_store_col + [pd.Grouper(key=date_col, freq=freq)])[target_col].sum().reset_index()
            df_temp[f"sales_expected_{sku_store_col_name}_{freq}"] = df_temp.groupby(sku_store_col)[
                target_col].transform(
                lambda x: x.mean()).shift(1).fillna(0)
            df_temp[f"sales_expected_{sku_store_col_name}_{freq}"] = df_temp[
                f"sales_expected_{sku_store_col_name}_{freq}"].replace(
                [np.inf, -np.inf], 0)
            df_expected = pd.concat(
                [df_expected, df_temp[[date_col] + sku_store_col + [f"sales_expected_{sku_store_col_name}_{freq}"]]])

        df = pd.merge(df, df_expected, on=[date_col] + sku_store_col, how='left').fillna(0)
        df = df.drop_duplicates(subset=sku_store_col + [date_col], keep='last')
        return df

    @classmethod
    def calculate_statistics_functions_per_sku_store(cls, df: pd.DataFrame, target_col: str, date_col: str,
                                                     sku_store_col: List[str],
                                                     window_size_list: List[int]) -> pd.DataFrame:

        df_stat_rolls = []
        group_data = df.groupby([date_col] + sku_store_col)[target_col]
        for window_size in window_size_list:
            df_stat_roll = group_data.rolling(window_size, min_periods=1).agg(
                ['mean', 'median', 'std', lambda x: x.quantile(0.25), lambda x: x.quantile(0.75)]).shift(1).fillna(
                0).reset_index()
            cols_to_drop = [col for col in df_stat_roll.columns if col.startswith('level')]
            df_stat_roll = df_stat_roll.drop(columns=cols_to_drop)
            col_names_roll = [f'{sku_store_col}_' + '_'.join([str(window_size), 'day', col]).strip() + '_shifted' for
                              col
                              in
                              ['mean', 'median', 'std', 'quantile_25', 'quantile_75']]
            df_stat_roll.columns = [[date_col] + sku_store_col + col_names_roll]
            for col in col_names_roll:
                col_name_roll = f'{col}_365_day_rolling_mean'
                df_stat_roll[col_name_roll] = df_stat_roll[col].rolling(365).mean().shift(1).fillna(0).reset_index()[
                    col]
            df_stat_rolls.append(df_stat_roll)
            print(f"window_size: {window_size}")
        df_stat_roll_concat = pd.concat(df_stat_rolls, axis=1)
        df_stat_roll_concat = df_stat_roll_concat.loc[:, ~df_stat_roll_concat.columns.duplicated()]
        df_stat_roll_concat.columns = ['_'.join(map(str, col)).rstrip('_') for col in
                                       df_stat_roll_concat.columns.values]
        df_stat_roll_concat = df_stat_roll_concat.reset_index(drop=True)
        print(f"orignal_data: {df.shape} after rolling: {df_stat_roll_concat.shape}")
        df = pd.merge(df, df_stat_roll_concat, on=sku_store_col + [date_col], how='left')
        df = df.drop_duplicates(subset=sku_store_col + [date_col], keep='last')
        print(f"orignal_data: {df.shape} after rolling: {df_stat_roll_concat.shape}")
        return df

    @classmethod
    def add_stats_functions_to_data(cls, df: pd.DataFrame, target_col: str, date_col: str, sku_store_col: List[str],
                                    window_size_list: List[int]) -> pd.DataFrame:
        for stat_col in sku_store_col:
            df_stat_rolls = []
            group_data = df.groupby([date_col, stat_col])[target_col]
            for window_size in window_size_list:
                df_stat_roll = group_data.rolling(window_size, min_periods=1).agg(
                    ['mean', 'median', 'std', lambda x: x.quantile(0.25), lambda x: x.quantile(0.75)]).shift(
                    1).fillna(
                    0).reset_index()
                cols_to_drop = [col for col in df_stat_roll.columns if col.startswith('level')]
                df_stat_roll = df_stat_roll.drop(columns=cols_to_drop)
                col_names_roll = [f'{stat_col}_' + '_'.join([str(window_size), 'day', col]).strip() + '_shifted' for
                                  col in
                                  ['mean', 'median', 'std', 'quantile_25', 'quantile_75']]
                df_stat_roll.columns = [[date_col, stat_col] + col_names_roll]
                for col in col_names_roll:
                    col_name_roll = f'{col}_365_day_rolling_mean'
                    df_stat_roll[col_name_roll] = \
                        df_stat_roll[col].rolling(365).mean().shift(1).fillna(0).reset_index()[
                            col]

                df_stat_rolls.append(df_stat_roll)
                print(f"window_size: {window_size}")
            df_stat_roll_concat = pd.concat(df_stat_rolls, axis=1)
            df_stat_roll_concat = df_stat_roll_concat.loc[:, ~df_stat_roll_concat.columns.duplicated()]
            df_stat_roll_concat.columns = ['_'.join(map(str, col)).rstrip('_') for col in
                                           df_stat_roll_concat.columns.values]
            df_stat_roll_concat = df_stat_roll_concat.reset_index(drop=True)
            print(f"orignal_data: {df.shape} after rolling: {df_stat_roll_concat.shape}")
            df = pd.merge(df, df_stat_roll_concat, on=[stat_col, date_col], how='left')
            df = df.drop_duplicates(subset=[stat_col, date_col], keep='last')
            print(f"orignal_data: {df.shape} after rolling: {df_stat_roll_concat.shape}")
            del df_stat_rolls
        return df

    #TODO: fix sku_store_col value to be unified across all project
    @classmethod
    def run_pipline_cumulative(cls, data_sales, target_col=config.SALES_COLUMN_NAME,
                               sku_store_col=['store', 'sku'], date_col=config.DATE_COLUMN_NAME,
                               list_freq=config.LIST_FREQ, start_date=config.START_DATE_CUMULATIVE_FEATURES):

        data_sales2 = cls.filter_data_by_date(data_sales, date_col, start_date)
        data_sales2 = cls.groupby_sum_sku_store(data_sales2, target_col, sku_store_col,
                                                                        date_col)
        data_sales2 = cls.add_cumulative_sum_column_respect_time(data_sales2,
                                                                 target_col, sku_store_col,
                                                                 list_freq,
                                                                 date_col)
        data_sales2 = cls.add_expected_value_column_respect_time(data_sales2, target_col,
                                                                 sku_store_col,
                                                                 list_freq, date_col)

        data_sales2.drop(columns=[target_col], inplace=True)
        return data_sales2




