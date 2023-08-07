from datetime import timedelta

import numpy as np
import pandas as pd
from . import config as global_config
from .features.event_features import EventFeaturesGenerator
from .features.future_features import FarFutureFeaturesGenerator
from .features.lags_features import SKULagFeatureGenerator, StoreLagFeatureGenerator, IDLagFeatureGenerator
from .features.weather_features import WeatherFeatureGenerator, StoreLocationLoader
from .regular_data_handler import RegularDataLoader, RegularDataProcessor
from .utils import parse_regular_data_columns, next_two_days_skip_sunday
from .features.cumulative_features import CumulativeFeatureGenerator




class Preprocessor:
    def __init__(self):
        pass

    @classmethod
    def get_future_rows(cls, regular_data_df, begin_date, end_date):
        unique_ids = regular_data_df[global_config.SKU_STORE_COLUMN_NAME].unique()

        dfs = []
        for date in pd.date_range(begin_date, end_date):
            df = pd.DataFrame(
                {global_config.SKU_STORE_COLUMN_NAME: unique_ids, global_config.DATE_COLUMN_NAME: date})
            df[[global_config.SKU_COLUMN_NAME, global_config.STORE_COLUMN_NAME]] = df[global_config.SKU_STORE_COLUMN_NAME].str.split(", ", expand=True)
            dfs.append(df)

        # future_df = pd.DataFrame(
        #     {global_config.SKU_STORE_COLUMN_NAME: unique_ids, global_config.DATE_COLUMN_NAME: begin_date})
        # future_df[[global_config.SKU_COLUMN_NAME, global_config.STORE_COLUMN_NAME]] = future_df[
        #     global_config.SKU_STORE_COLUMN_NAME].str.split(", ", expand=True)

        return pd.concat(dfs)


    @classmethod
    def create_store_id_dict(cls, regular_data_df):
        sku_store_dict = regular_data_df.groupby(global_config.STORE_COLUMN_NAME)[global_config.SKU_STORE_COLUMN_NAME].unique().apply(list).to_dict()
        return sku_store_dict

    @classmethod
    def preprocess(cls, stores_list=global_config.OUTLETS_SDATTA, begin_predict_dates = '2023-01-01', regular_data_df=None):
        """

        :param stores_list: list of ints of store ids
        :param begin_predict_dates:
        :param regular_data_df:
        :return:
        """
        if pd.to_datetime(begin_predict_dates).strftime("%A") == "Sunday":
            print("predict_date is Sunday, no need to predict")
            return

        if regular_data_df is None:
            regular_data_df = RegularDataLoader().load()


        # TODO: seperate the two days being added for events

        future_df = cls.get_future_rows(regular_data_df, begin_predict_dates, begin_predict_dates)
        regular_data_df = pd.concat([regular_data_df, future_df], ignore_index=True)
        regular_data_df = parse_regular_data_columns(regular_data_df)


        final_event_features_df = EventFeaturesGenerator().generate(regular_data_df, begin_predict_dates=begin_predict_dates)



        #TODO: first load store_location_here, then call weather prediction someplace else.
        #store_location_df = StoreLocationLoader().load() # on all stores
        cumulative_features_df = cls.get_cumulative_features(regular_data_df)


        sku_lags_features_df = SKULagFeatureGenerator().create_all_sku_lags(regular_data_df, begin_predict_dates)


        # TODO: after the sku_lags, we can filter the regular data (Check this!!!!!)
        regular_data_df = regular_data_df[regular_data_df[global_config.STORE_COLUMN_NAME].isin(stores_list)]

        store_id_dict = cls.create_store_id_dict(regular_data_df)
        far_future_features_df = FarFutureFeaturesGenerator().far_future_features_preprocess_of_several_stores(store_batch_dict=store_id_dict, begin_predict_dates=begin_predict_dates)


        all_ids_data_for_predict_date = pd.DataFrame()
        for store in stores_list:
            all_id_data_in_store = pd.DataFrame()
            store_data_df = regular_data_df[regular_data_df[global_config.STORE_COLUMN_NAME] == store]
            # load future features
            store_future_features = far_future_features_df[store] # feature
            store_lags_df = StoreLagFeatureGenerator().create_all_stores_lags(store_data_df, predict_date=begin_predict_dates) # feature
            stores_weather_df = WeatherFeatureGenerator().generate(store_id=store, start_predict_date=begin_predict_dates, end_predict_date = begin_predict_dates)

            for sku in store_data_df[global_config.SKU_COLUMN_NAME].unique():
                _id = str(sku) + ", " + str(store)
                id_data_df = store_data_df[store_data_df[global_config.SKU_STORE_COLUMN_NAME] == _id]

                id_data_df = IDLagFeatureGenerator().create_id_lags(id_data_df=id_data_df, sku=sku, store=store, predict_date=begin_predict_dates) # feature
                #id_data_df[global_config.SKU_STORE_COLUMN_NAME] = _id
                all_id_data_in_store = pd.concat([all_id_data_in_store, id_data_df])

            all_id_data_in_store = all_id_data_in_store.merge(store_future_features,
                                                              on=[global_config.DATE_COLUMN_NAME, global_config.SKU_COLUMN_NAME, global_config.STORE_COLUMN_NAME],
                                                              how="left")

            all_id_data_in_store = all_id_data_in_store.merge(store_lags_df,
                                                              on=[global_config.DATE_COLUMN_NAME],
                                                              how="left")
            all_id_data_in_store = all_id_data_in_store.merge(stores_weather_df, on=[global_config.DATE_COLUMN_NAME, global_config.STORE_COLUMN_NAME],
                                                              how="left")

            all_id_data_in_store = all_id_data_in_store.merge(cumulative_features_df,on=[global_config.DATE_COLUMN_NAME, global_config.SKU_COLUMN_NAME, global_config.STORE_COLUMN_NAME], how="left")

            all_ids_data_for_predict_date = pd.concat([all_ids_data_for_predict_date, all_id_data_in_store])

        all_ids_data_for_predict_date = all_ids_data_for_predict_date.merge(sku_lags_features_df,
                                                                            on=[global_config.DATE_COLUMN_NAME,
                                                                                global_config.SKU_COLUMN_NAME,
                                                                                ],
                                                                            how="left")



        all_ids_data_for_predict_date = all_ids_data_for_predict_date.merge(final_event_features_df, on=[global_config.DATE_COLUMN_NAME],
                                                                            how="left")

        all_ids_data_for_predict_date.columns = all_ids_data_for_predict_date.columns.str.replace(':', '')

        # drop unnecessary columns
        cols_to_drop = [col for col in all_ids_data_for_predict_date.columns if 'MEST_all_time' in col
                        or 'months_5_6_7' in col or col == 'index']
        all_ids_data_for_predict_date.drop(cols_to_drop, axis=1, inplace=True)

        return all_ids_data_for_predict_date


    @classmethod
    def get_cumulative_features(cls, regular_data_df):
        cumulative_features = CumulativeFeatureGenerator().run_pipline_cumulative(regular_data_df)
        cumulative_features = parse_regular_data_columns(cumulative_features)
        return cumulative_features






