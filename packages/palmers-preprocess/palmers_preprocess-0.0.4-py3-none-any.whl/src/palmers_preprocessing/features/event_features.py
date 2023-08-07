import pandas as pd

from .. import config as global_config
from ..clearml_data_handler import ArtifactLoader, DatasetLoader
from .. import events_handler as eh
from ..utils import next_two_days_skip_sunday, parse_regular_data_columns


class EventEncodingFeaturesLoader:
    @classmethod
    def load(cls, project_name=global_config.DEFAULT_EVENT_ENCODING_FEATURES['project_name'],
             task_name=global_config.DEFAULT_EVENT_ENCODING_FEATURES['task_name'],
             task_id=global_config.DEFAULT_EVENT_ENCODING_FEATURES['task_id'],
             artifacts_names=global_config.DEFAULT_EVENT_ENCODING_FEATURES['artifacts_names']):

        encoded_artifacts = ArtifactLoader().load_pickle_artifacts(project_name=project_name,
                                                                  task_name=task_name,
                                                                  task_id=task_id,
                                                                  artifacts_names=artifacts_names)

        return encoded_artifacts


class EventHistoryFeatureLoader:
    @classmethod
    def load(cls, dataset_project=global_config.DEFAULT_EVENT_DATASET['dataset_project'],
             dataset_name=global_config.DEFAULT_EVENT_DATASET['dataset_name'],
             dataset_version=global_config.DEFAULT_EVENT_DATASET['dataset_version'],
             dataset_tags=global_config.DEFAULT_EVENT_DATASET['dataset_tags'],
             dataset_file_name=global_config.DEFAULT_EVENT_DATASET['dataset_file_name']):
        events_files = DatasetLoader().load_dfs_from_dataset(dataset_project=dataset_project,
                                                                   dataset_name=dataset_name,
                                                                   dataset_version=dataset_version,
                                                                   dataset_tags=dataset_tags,
                                                                   dataset_file_names=[dataset_file_name])

        events_df = events_files[dataset_file_name]
        return events_df

class HolidayFeaturesLoader:
    @classmethod
    def load(cls, dataset_project=global_config.DEFAULT_HOLIDAYS_DATASET['dataset_project'],
             dataset_name=global_config.DEFAULT_HOLIDAYS_DATASET['dataset_name'],
             dataset_version=global_config.DEFAULT_HOLIDAYS_DATASET['dataset_version'],
             dataset_tags=global_config.DEFAULT_HOLIDAYS_DATASET['dataset_tags'],
             dataset_file_name=global_config.DEFAULT_HOLIDAYS_DATASET['dataset_file_name']):
        holiday_files = DatasetLoader().load_dfs_from_dataset(dataset_project=dataset_project,
                                                             dataset_name=dataset_name,
                                                             dataset_version=dataset_version,
                                                             dataset_tags=dataset_tags,
                                                             dataset_file_names=[dataset_file_name])

        holiday_df = holiday_files[dataset_file_name]
        return holiday_df



class EventFeaturesGenerator:
    @classmethod
    def apply_encoder(cls, df, encoder, columns, columns_after_apply, fillna=False):
        if fillna:
            df[columns_after_apply] = encoder.transform(df[columns].fillna(0))
        else:
            df[columns_after_apply] = encoder.transform(df[columns])

        return df

    @classmethod
    def perform_encoders(cls, processed_event_features_df, event_encoders):
        # pca
        pca_dict = event_encoders[global_config.PCA_ENCODER_ARTIFACT_NAME]['pca_weights']
        cls.apply_encoder(df=processed_event_features_df,
                          encoder=pca_dict['pca'],
                          columns=pca_dict['columns'],
                          columns_after_apply=pca_dict['columns_after_apply'],
                          fillna=True)

        # apply encodings
        apply_encoding_dict = event_encoders[global_config.APPLY_ENCODINGS_DICT_ARTIFACT_NAME]
        for key in apply_encoding_dict.keys():
            encoder_dict = apply_encoding_dict[key]
            cls.apply_encoder(df=processed_event_features_df,
                              encoder=encoder_dict['encoder'],
                              columns=encoder_dict['columns'],
                              columns_after_apply=key)

        # apply_encoding_at_once_dict
        for encoder_name in ['MEstimateEncoder', 'CatBoostEncoder']:
            encoder_model = event_encoders[global_config.APPLY_ENCODINGS_AT_ONCE_ARTIFACT_NAME][encoder_name]
            cls.apply_encoder(df=processed_event_features_df,
                              encoder=encoder_model['encoder'],
                              columns=encoder_model['columns'],
                              columns_after_apply=encoder_model['columns_after_apply']
                              )

        # interactions
        processed_event_features_df = eh.create_interactions_columns(processed_event_features_df)
        for encoder_name in ['MEstimateEncoder', 'CatBoostEncoder']:
            encoder_model = event_encoders[global_config.COLUMNS_INTERACTIONS_ENCODER_ARTIFACT_NAME][encoder_name]
            cls.apply_encoder(df=processed_event_features_df,
                              encoder=encoder_model['encoder'],
                              columns=encoder_model['columns'],
                              columns_after_apply=encoder_model['columns_after_apply']
                              )
        return processed_event_features_df




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
    def generate_event_features(cls, regular_data_df, event_df, holiday_df, begin_predict_dates): #, min_date, max_date):

        #add two days
        start_date = next_two_days_skip_sunday(begin_predict_dates)[0]
        end_date = next_two_days_skip_sunday(begin_predict_dates)[-1]
        future_df = cls.get_future_rows(regular_data_df, start_date, end_date)
        df_with2days = pd.concat([regular_data_df, future_df], ignore_index=True)
        df_with2days = parse_regular_data_columns(df_with2days)

        # init pipeline
        processed_event_features_df = eh.run_pipline_event(data_event=event_df, data_sales=df_with2days, data_hol=holiday_df) #, min_date=min_date, max_date=max_date)

        # load & apply encoders
        event_encoders = EventEncodingFeaturesLoader.load()
        processed_event_features_df = cls.perform_encoders(processed_event_features_df, event_encoders)

        # finalize pipeline
        processed_event_features_df = eh.finalize_data(processed_event_features_df) #, min_date=min_date, max_date=max_date)


        df_final_event_features = processed_event_features_df.loc[:,
                                  ~processed_event_features_df.columns.str.contains('Unnamed')]

        df_final_event_features[global_config.DATE_COLUMN_NAME] = pd.to_datetime(
            df_final_event_features[global_config.DATE_COLUMN_NAME])
        df_final_event_features.set_index(global_config.DATE_COLUMN_NAME, inplace=True)

        df_final_event_features.fillna(0, inplace=True)
        df_final_event_features.reset_index(inplace=True)

        processed_event_features_df = processed_event_features_df[
            processed_event_features_df[global_config.DATE_COLUMN_NAME] == begin_predict_dates]
        return processed_event_features_df


    @classmethod
    def generate(cls, regular_data_df, begin_predict_dates):
        event_df = EventHistoryFeatureLoader.load()
        holiday_df = HolidayFeaturesLoader.load()
        processed_event_features_df = cls.generate_event_features(regular_data_df, event_df, holiday_df, begin_predict_dates=begin_predict_dates)
        processed_event_features_df = processed_event_features_df[processed_event_features_df[global_config.DATE_COLUMN_NAME] == begin_predict_dates]
        processed_event_features_df.drop(columns=[global_config.SALES_COLUMN_NAME], inplace=True)
        return processed_event_features_df


