import sys

from src.palmers_preprocessing.preprocessor import Preprocessor
from src.palmers_preprocessing.regular_data_handler import RegularDataLoader

sys.path.append('../src')
from src.palmers_preprocessing.features.event_features import EventHistoryFeatureLoader, EventFeaturesGenerator, \
    EventEncodingFeaturesLoader
import src.palmers_preprocessing.config as global_config


def test_event_features_load():
    event_feature_df = EventHistoryFeatureLoader.load(project_name=global_config.DEFAULT_EVENT_FEATURES['project_name'],
                                                      task_name=global_config.DEFAULT_EVENT_FEATURES['task_name'],
                                                      task_id=global_config.DEFAULT_EVENT_FEATURES['task_id'],
                                                      artifact_name=global_config.DEFAULT_EVENT_FEATURES['artifact_name'])

    print(event_feature_df)
    print(event_feature_df.columns)


def test_event_features_generate():
    generator = EventFeaturesGenerator()
    preprocessor = Preprocessor()
    stores = ['4906', '3']
    df = RegularDataLoader().load()
    df = df[df['store'].isin(stores)]
    skus_1 = df[df['store'] == '4906']['sku'].unique()[0:5]
    skus_2 = df[df['store'] == '3']['sku'].unique()[0:5]
    df = df[df['sku'].isin(skus_1) | df['sku'].isin(skus_2)]

    df = generator.generate(regular_data_df = df)
    print(df)
    print(df.info())


def test_event_encoding_features_loader():
    artifacts = EventEncodingFeaturesLoader().load()

    model3 = artifacts['apply_encodings_dict']
    print(model3)

    # print(artifacts.keys())
    # model1 = artifacts['apply_encodings_at_once']
    # print(model1)
    # model2 = artifacts['apply_encodings_dict']
    # print(model2)
    #
    # model4 = artifacts['pca_dict']
    # print(model4)

test_event_features_generate()
#test_event_features_load()
#test_event_encoding_features_loader()


