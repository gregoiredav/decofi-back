DEPT_OUTREMER = ['101', '102', '103', '104', '106']


class Cleaner(object):
    """
    Cette classe inclut un certain nombre de fonctions crées pour nettoyer les données des balances comptables des
    collectivités locales, une fois le csv converti au format Pandas DataFrame.

    Elle est initiée avec un dictionnaire qui associe un nom de colonne de DataFrame à une fonction qui sera appliquée
    à chaque colonne.
    """

    def __init__(self, actions):
        self.actions = actions

    def clean(self, df):
        """
        Applique les différentes fonctions du Cleaner.

        :param df: pandas DataFrame contenant les balances comptables.
        :return: clean DataFrame
        """
        for col, action in self.actions.items():
            df[col] = df[col].apply(action)
        return df

    @staticmethod
    def chiffre(ligne):
        return float(ligne.replace(',', '.'))

    @staticmethod
    def insee(ligne):
        if ligne.startswith('`'):
            return ligne[1:]
        return ligne

    @staticmethod
    def fonction(ligne):
        if ligne == '':
            return '000'
        else:
            return (
                ligne
                .replace('-', '')
                .replace('.', '')
            )

    @staticmethod
    def ndept(ligne):
        if ligne in DEPT_OUTREMER:
            ligne = "097"
        return ligne[1:]
