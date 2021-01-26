import pickle
import pandas as pd


def get_pickle_path(filename):
    return f'../pickles/{filename}.pickle'


def set_pickle(data, filename):
    path = get_pickle_path(filename)
    if isinstance(data, pd.DataFrame):
        data.to_pickle(path)
        return

    with open(path, 'wb') as f:
        pickle.dump(data, f)


def get_pickle(filename):
    with open(get_pickle_path(filename), 'rb') as f:
        return pickle.load(f)


