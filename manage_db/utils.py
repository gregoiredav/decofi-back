from datetime import datetime

import numpy as np


def time_operation(function):
    """
    A utiliser comme decorator autour d'une fonction pour enregistrer son temps d'exécution

    :param function: fonction à timer
    :return: fonction
    """
    def timed_operation(*args, **kwargs):
        ts = datetime.now()
        result = function(*args, **kwargs)
        te = datetime.now()

        if 'log_time' in kwargs:
            name = kwargs.get('log_name', function.__name__.upper())
            kwargs['log_time'][name] = str(te - ts)
        else:
            print(f"{function.__name__}: {str(te - ts)}")
        return result
    return timed_operation


def batch_dataframe(df, split_col, nr_splits):
    """
    Utilitaire splittant un DataFrame sur la base des valeurs d'une colonne, pour pouvoir créer des batchs.

    :param df: pandas DataFrame à splitter
    :param split_col: colonne qui servira à trier et splitter
    :param nr_splits: nombres de batch
    :return: liste de DataFrame
    """
    df.sort_values(by=split_col, inplace=True)
    code_insee_array = df[split_col].unique()
    code_insee_splits = np.array_split(code_insee_array, nr_splits)
    df_splits = map(lambda split: df[df[split_col].isin(split)], code_insee_splits)
    return list(df_splits)