import joblib
import seaborn as sns
import pandas as pd
import numpy as np

def preprocessing(df_main):

    df_main['Open_sf_1'] = np.log(df_main['Open']/df_main['Open'].shift(1)).values
    df_main['Open_sf_6'] = np.log(df_main['Open']/df_main['Open'].shift(6)).values
    df_main['Open_sf_12'] = np.log(df_main['Open']/df_main['Open'].shift(12)).values

    df_main['exp_moving_avg'] = round(df_main['Open'].ewm(alpha=0.5, adjust=False).mean(), 2)
    df_main['moving_avg_6'] = df_main['Open'].rolling(6).mean()
    df_main['moving_avg_12'] = df_main['Open'].rolling(12).mean()
    df_main['moving_avg_24'] = df_main['Open'].rolling(24).mean()

    df_main[['moving_avg_6_tf', 'moving_avg_12_tf', 'moving_avg_24_tf']] = np.log(df_main[['moving_avg_6', 'moving_avg_12', 'moving_avg_24']]/df_main[['moving_avg_6', 'moving_avg_12', 'moving_avg_24']].shift(1)).values

    df_main['min_6'] = df_main['Open'].rolling(6).min()
    df_main['min_12'] = df_main['Open'].rolling(12).min()
    df_main['min_24'] = df_main['Open'].rolling(24).min()

    df_main['max_6'] = df_main['Open'].rolling(6).max()
    df_main['max_12'] = df_main['Open'].rolling(12).max()
    df_main['max_24'] = df_main['Open'].rolling(24).max()

    df_main['max_min_6'] = df_main['max_6'] - df_main['min_6']
    df_main['max_min_12'] = df_main['max_12'] - df_main['min_12']
    df_main['max_min_24'] = df_main['max_24'] - df_main['min_24']

    return df_main

def get_predictions(model, data):

    clf = joblib.load(model)

    data = pd.DataFrame(data, columns=['Open'])
    data = preprocessing(data.copy())
    cols = ['Open_sf_1', 'Open_sf_6', 'Open_sf_12',
            'exp_moving_avg', 'moving_avg_6', 'max_min_6', 'max_min_12',
            'max_min_24', 'moving_avg_6_tf', 'moving_avg_12_tf', 'moving_avg_24_tf']
    X_test = data[cols].iloc[24:]

    scores_test = clf.score_samples(X_test)
    labels_test = np.where(scores_test < -0.63, -1, 1)

    X_test[["labels"]] = 1
    for i, val in enumerate(labels_test):
        X_test.iloc[i, -1] = val

    return X_test