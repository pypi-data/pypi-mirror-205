import sys

from src.palmers_preprocessing.regular_data_handler import RegularDataLoader

sys.path.append('../src')
from src.palmers_preprocessing.preprocessor import Preprocessor


def test_prepreocessor():
    preprocessor = Preprocessor()
    stores = ['4906', '3']
    df = RegularDataLoader().load()
    df = df[df['store'].isin(stores)]
    skus_1 = df[df['store'] == '4906']['sku'].unique()[0:5]
    skus_2 = df[df['store'] == '3']['sku'].unique()[0:5]
    df = df[df['sku'].isin(skus_1) | df['sku'].isin(skus_2)]

    df = preprocessor.preprocess(stores_list=[4906, 3], begin_predict_dates='2023-04-24', regular_data_df=df)

    print(df)
    print(df.columns.tolist())

def test_cumulative_features():
    preprocessor = Preprocessor()
    df = preprocessor.get_regular_data_of_store(store_id='109', predict_date='2023-04-24')
    cum_feat = preprocessor.get_cumulative_features(df)
    print(cum_feat)

test_prepreocessor()

