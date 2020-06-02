class Cleaner(object):

    def __init__(self, actions):
        self.actions = actions

    def clean(self, df):
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
        if ligne.startswith('0'):
            ligne = ligne[1:]
        return ligne
