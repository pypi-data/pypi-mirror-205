# from clearml_architecture.feature_process.WeatherFeatures.global_config import *
from clearml import Dataset, Task
import pandas as pd

from .. import config as global_config
from . import config

from ..clearml_data_handler import DatasetLoader, ArtifactLoader
from ..utils import process_date_column, add_values_to_dict_mapper, map_encoders_columns_to_base_df

class MarketingPlanFeatures:
    @classmethod
    def load(cls, project_name=global_config.DEFAULT_MARKETING_PLAN_FEATURES['project_name'],
             task_name=global_config.DEFAULT_MARKETING_PLAN_FEATURES['task_name'],
             task_id=global_config.DEFAULT_MARKETING_PLAN_FEATURES['task_id'],
             artifact_name=global_config.DEFAULT_MARKETING_PLAN_FEATURES['artifact_name'],
             ):

        marketing_plan_df = ArtifactLoader().load_artifact_as_df(project_name=project_name,
                                                                   task_name=task_name,
                                                                   task_id=task_id,
                                                                   artifact_name=artifact_name,
                                                                   )
        marketing_plan_df = marketing_plan_df.loc[:,
                                   ~marketing_plan_df.columns.str.contains('Unnamed')]
        marketing_plan_df = marketing_plan_df.dropna()

        cols_to_convert = marketing_plan_df.columns.difference(['date'])
        marketing_plan_df[cols_to_convert] = marketing_plan_df[cols_to_convert].astype('int32')

        return marketing_plan_df


class SkuSaleEncodedFeatures:
    @classmethod
    def load(cls, task_id=global_config.DEFAULT_SKU_SALE_ENCODED_FEATURES['task_id'],
             project_name=global_config.DEFAULT_SKU_SALE_ENCODED_FEATURES['project_name'],
             task_name=global_config.DEFAULT_SKU_SALE_ENCODED_FEATURES['task_name'],
             artifact_name=global_config.DEFAULT_SKU_SALE_ENCODED_FEATURES['artifact_name']):
        sku_encoders = ArtifactLoader().load_artifact_as_df(project_name=project_name,
                                                            task_name=task_name,
                                                            task_id=task_id,
                                                            artifact_name=artifact_name)
        sku_encoders = sku_encoders.drop('Unnamed: 0', axis=1)
        sku_encoders[global_config.SKU_COLUMN_NAME] = sku_encoders[global_config.SKU_COLUMN_NAME].astype('int64')
        sku_encoders = sku_encoders.set_index(global_config.SKU_COLUMN_NAME)
        sku_encoders = sku_encoders.astype('float')

        return sku_encoders


class StoreSaleEncodedFeatures:
    @classmethod
    def load(cls, task_id=global_config.DEFAULT_STORE_SALE_ENCODED_FEATURES['task_id'],
             project_name=global_config.DEFAULT_STORE_SALE_ENCODED_FEATURES['project_name'],
             task_name=global_config.DEFAULT_STORE_SALE_ENCODED_FEATURES['task_name'],
             artifact_name=global_config.DEFAULT_STORE_SALE_ENCODED_FEATURES['artifact_name']):
        store_encoders =  ArtifactLoader().load_artifact_as_df(project_name=project_name,
                                                            task_name=task_name,
                                                            task_id=task_id,
                                                            artifact_name=artifact_name)
        store_encoders = store_encoders.drop('Unnamed: 0', axis=1)
        store_encoders[global_config.STORE_COLUMN_NAME] = store_encoders[global_config.STORE_COLUMN_NAME].astype('int32')
        store_encoders = store_encoders.set_index(global_config.STORE_COLUMN_NAME)
        store_encoders=store_encoders.astype('float')

        return store_encoders



class FarFutureFeaturesGenerator:

    @classmethod
    def far_future_features_preprocess_of_store(cls, store_batch, begin_predict_dates):
        marketing_plan = MarketingPlanFeatures.load()
        sku_encoders =  SkuSaleEncodedFeatures.load()#.reset_index().rename(columns={'index': global_config.SKU_COLUMN_NAME})
        store_encoders =  StoreSaleEncodedFeatures.load()#.reset_index().rename(columns={'index': global_config.STORE_COLUMN_NAME})


        dict_mapper = add_values_to_dict_mapper(config.DICT_MAPPER, sku_encoders, global_config.SKU_COLUMN_NAME, config.ENCODERS_NAME,
                                              config.DICT_OF_TIME_INTERVAL)

        dict_mapper = add_values_to_dict_mapper(dict_mapper, store_encoders, global_config.STORE_COLUMN_NAME, config.ENCODERS_NAME,
                                              config.DICT_OF_TIME_INTERVAL)



        future_date_range = pd.date_range(start=begin_predict_dates, end=begin_predict_dates, freq='D')

        output_df = pd.DataFrame()
        for _id in store_batch:
            sku_store_id = _id
            sku = int(sku_store_id.split(',')[0])
            store = int(sku_store_id.split(',')[1])
            id_data_future = pd.DataFrame({'date': future_date_range,
                                           'sku, store': sku_store_id,
                                           'sku': sku,
                                           'store': store})

            id_data_future = process_date_column(id_data_future, global_config.DATE_COLUMN_NAME, expanded=True)

            # Exclude Sunday
            #id_data_future = id_data_future[id_data_future['day_of_week'] != 6]

            marketing_plan[global_config.DATE_COLUMN_NAME] = pd.to_datetime(marketing_plan[global_config.DATE_COLUMN_NAME])

            id_data_future = pd.merge(id_data_future, marketing_plan, on=[global_config.DATE_COLUMN_NAME], how='left')

            id_data_future = map_encoders_columns_to_base_df(id_data_future, dict_mapper, config.ENCODERS_NAME)
            output_df = pd.concat([output_df, id_data_future])

        #output_df.drop('name_of_day', axis=1, inplace=True)
        return output_df

    @classmethod
    def far_future_features_preprocess_of_several_stores(cls, store_batch_dict, begin_predict_dates):
        marketing_plan = MarketingPlanFeatures.load()
        sku_encoders = SkuSaleEncodedFeatures.load()
        store_encoders = StoreSaleEncodedFeatures.load()

        dict_mapper = add_values_to_dict_mapper(config.DICT_MAPPER, sku_encoders, global_config.SKU_COLUMN_NAME,
                                                config.ENCODERS_NAME,
                                                config.DICT_OF_TIME_INTERVAL)

        dict_mapper = add_values_to_dict_mapper(dict_mapper, store_encoders, global_config.STORE_COLUMN_NAME,
                                                config.ENCODERS_NAME,
                                                config.DICT_OF_TIME_INTERVAL)

        future_date_range = pd.date_range(start=begin_predict_dates, end=begin_predict_dates, freq='D')

        output_dfs = {}
        for store_id in list(store_batch_dict.keys()):
            output_df = pd.DataFrame()
            for _id in store_batch_dict[store_id]:
                sku_store_id = _id
                sku = int(sku_store_id.split(',')[0])
                store = int(sku_store_id.split(',')[1])
                id_data_future = pd.DataFrame({'date': future_date_range,
                                               'sku, store': sku_store_id,
                                               'sku': sku,
                                               'store': store})
                id_data_future = process_date_column(id_data_future, global_config.DATE_COLUMN_NAME, expanded=True)

                # Exclude Sunday
                # id_data_future = id_data_future[id_data_future['day_of_week'] != 6]

                marketing_plan[global_config.DATE_COLUMN_NAME] = pd.to_datetime(marketing_plan[global_config.DATE_COLUMN_NAME])
                id_data_future = pd.merge(id_data_future, marketing_plan, on=[global_config.DATE_COLUMN_NAME], how='left')
                id_data_future = map_encoders_columns_to_base_df(id_data_future, dict_mapper, config.ENCODERS_NAME)
                output_df = pd.concat([output_df, id_data_future])

            #output_df.drop('name_of_day', axis=1, inplace=True)
            output_dfs[store_id] = output_df

        return output_dfs