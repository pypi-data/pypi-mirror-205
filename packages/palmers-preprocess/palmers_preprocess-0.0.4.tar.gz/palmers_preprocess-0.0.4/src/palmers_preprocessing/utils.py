from datetime import timedelta, datetime

import numpy as np
import pandas as pd
from . import config

def process_date_column(df_sales: pd.DataFrame, date_col: str, expanded:bool = False) -> pd.DataFrame:
    """
    Process date column
    Args:
        df_sales: pandas DataFrame
        date_col: name of date column
    Returns: pandas DataFrame
    """
    df_sales[date_col] = pd.to_datetime(df_sales[date_col])
    df_sales['year'] = df_sales[date_col].dt.year
    df_sales['month'] = df_sales[date_col].dt.month
    df_sales['day'] = df_sales[date_col].dt.day
    df_sales['day_of_week'] = df_sales[date_col].dt.dayofweek
    df_sales['week_of_year'] = df_sales[date_col].apply(lambda x: x.isocalendar()[1])
    df_sales['quarter'] = df_sales[date_col].dt.quarter
    df_sales['is_weekend'] = df_sales[date_col].dt.dayofweek.isin([5, 6]).astype(int)
    df_sales['name_of_day'] = df_sales[date_col].dt.strftime("%A")

    if expanded:
        df_sales['day_of_year'] = df_sales[date_col].dt.dayofyear
        df_sales['day_of_the_month'] = df_sales[date_col].dt.days_in_month
        df_sales['is_weekend_c'] = df_sales['day_of_week'].apply(lambda x: 1 if x in [5, 6] else 0)
        df_sales['is_weekend_j'] = df_sales['day_of_week'].apply(lambda x: 1 if x in [4, 5] else 0)


    return df_sales


def add_values_to_dict_mapper(dict_mapper: dict, df_encoders: pd.DataFrame, column_name: str, encoders_name: list,
                             dict_of_time_interval: dict) -> dict:
    """
    Adds the values of the encoders in the df_encoders dataframe to the dict_maper dictionary.

    Args:
        dict_mapper:     The dictionary that holds the encoded values.
        df_encoders:        The dataframe that holds the encoded values.
        column_name:    The name of the column in the df_encoders dataframe.
        encoders_name:  The names of the encoders in the df_encoders dataframe.
        dict_of_time_interval:  The dictionary that holds the time intervals.

    Returns:    The updated dict_maper dictionary.

    """
    item_encoders_with_item_index = df_encoders.rename_axis(column_name)
    for item in df_encoders.index:
        for time in dict_of_time_interval:
            for date in dict_of_time_interval[time]:
                for encoder in encoders_name:
                    if time == "months_5_6_7":
                        dict_mapper[column_name][encoder]["months_5_6_7"][(item, date)] = \
                            item_encoders_with_item_index.loc[item][encoder + "_months:5_6_7"]
                    elif time == "all":
                        dict_mapper[column_name][encoder]["all"][(item, date)] = \
                            item_encoders_with_item_index.loc[item][encoder + "_all_time:all_time"]
                    else:
                        dict_mapper[column_name][encoder][time][(item, date)] = \
                            item_encoders_with_item_index.loc[item][encoder + "_" + str(time) + ":" + str(date)]
    return dict_mapper


def map_encoders_columns_to_base_df( data: pd.DataFrame, dict_map: dict, encoders_name: list) -> pd.DataFrame:
    """
    Adds the encoded values to the data dataframe.
    Args:
        data:   The dataframe to add the encoded values to.
        dict_map:   The dictionary that holds the encoded values.
        encoders_name:  The names of the encoders in the df_encoders dataframe.

    Returns:    The updated data dataframe.

    """
    for encoder_name in encoders_name:
        data[encoder_name + "_day_store"] = data.apply(
            lambda x: dict_map["store"][encoder_name]["name_of_day"][x["store"], x["name_of_day"]], axis=1)
        data[encoder_name + "_day_sku"] = data.apply(
            lambda x: dict_map["sku"][encoder_name]["name_of_day"][x["sku"], x["name_of_day"]], axis=1)
        data[encoder_name + "_month_store"] = data.apply(
            lambda x: dict_map["store"][encoder_name]["month"][x["store"], x["month"]], axis=1)
        data[encoder_name + "_month_sku"] = data.apply(
            lambda x: dict_map["sku"][encoder_name]["month"][x["sku"], x["month"]], axis=1)
        data[encoder_name + "_quarter_store"] = data.apply(
            lambda x: dict_map["store"][encoder_name]["quarter"][x["store"], x["quarter"]], axis=1)
        data[encoder_name + "_quarter_sku"] = data.apply(
            lambda x: dict_map["sku"][encoder_name]["quarter"][x["sku"], x["quarter"]], axis=1)
        data[encoder_name + "_months_5_6_7_store"] = data.apply(
            lambda x: dict_map["store"][encoder_name]["months_5_6_7"][x["store"], 0], axis=1)
        data[encoder_name + "_months_5_6_7_sku"] = data.apply(
            lambda x: dict_map["sku"][encoder_name]["months_5_6_7"][x["sku"], 0], axis=1)
        data[encoder_name + "_all_time_store"] = data.apply(
            lambda x: dict_map["store"][encoder_name]["all"][x["store"], 0], axis=1)
        data[encoder_name + "_all_time_sku"] = data.apply(
            lambda x: dict_map["sku"][encoder_name]["all"][x["sku"], 0], axis=1)

        data[encoder_name + "_day_store"] = data[encoder_name + "_day_store"].astype("float")
        data[encoder_name + "_day_sku"] = data[encoder_name + "_day_sku"].astype("float")
        data[encoder_name + "_month_store"] = data[encoder_name + "_month_store"].astype("float")
        data[encoder_name + "_month_sku"] = data[encoder_name + "_month_sku"].astype("float")
        data[encoder_name + "_quarter_store"] = data[encoder_name + "_quarter_store"].astype("float")
        data[encoder_name + "_quarter_sku"] = data[encoder_name + "_quarter_sku"].astype("float")
        data[encoder_name + "_months_5_6_7_store"] = data[encoder_name + "_months_5_6_7_store"].astype("float")
        data[encoder_name + "_months_5_6_7_sku"] = data[encoder_name + "_months_5_6_7_sku"].astype("float")
        data[encoder_name + "_all_time_store"] = data[encoder_name + "_all_time_store"].astype("float")
        data[encoder_name + "_all_time_sku"] = data[encoder_name + "_all_time_sku"].astype("float")

        return data

def parse_regular_data_columns(data: pd.DataFrame, sku_col_str = config.SKU_COLUMN_NAME, store_col_str=config.STORE_COLUMN_NAME,
                                   sales_col_str=config.SALES_COLUMN_NAME, date_col_str=config.DATE_COLUMN_NAME,
                               sku_store_col_str=config.SKU_STORE_COLUMN_NAME):
    if sku_col_str in data.columns:
        data[sku_col_str] = data[sku_col_str].astype(np.int64)
    if store_col_str in data.columns:
        data[store_col_str] = data[store_col_str].astype(np.int32)
    if sales_col_str in data.columns:
        data[sales_col_str] = data[sales_col_str].astype(np.float32)
    if date_col_str in data.columns:
        data[date_col_str] = pd.to_datetime(data[date_col_str])
    if sku_store_col_str in data.columns:
        data[sku_store_col_str] = data[sku_store_col_str].astype(str)
    return data

def next_two_days_skip_sunday(start_date):
    # Create a list to store the dates
    dates = []
    # parse start_date to datetime
    start_date = datetime.strptime(start_date, '%Y-%m-%d')

    # Loop through the next two days
    for i in range(2):
        # Add a day to the date
        start_date += timedelta(days=1)
        # Check if the new date is a Sunday
        if start_date.weekday() == 6:
            # If it's a Sunday, add another day to skip it
            start_date += timedelta(days=1)
        # Add the date to the list
        dates.append(start_date)



    # Return the dataframe
    return dates