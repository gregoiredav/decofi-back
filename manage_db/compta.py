AGGREGATS_COMPTE_DEPENSES = {
    -1: {
        'libelle': 'Pas une dépense',
        'comptes_a_inclure': [],
        'comptes_a_exclure': [],
    },
    1: {
        'libelle': 'Achats et charges externes',
        'comptes_a_inclure': ['60', '61', '62'],
        'comptes_a_exclure': ['621'],
    },
    2: {
        'libelle': 'Impôts et taxes',
        'comptes_a_inclure': ['63'],
        'comptes_a_exclure': ['631', '633'],
    },
    3: {
        'libelle': 'Charges de personnel',
        'comptes_a_inclure': ['64', '621', '631', '633'],
        'comptes_a_exclure': [],
    },
    4: {
        'libelle': 'Autres charges de gestion courante',
        'comptes_a_inclure': ['65'],
        'comptes_a_exclure': [],
    },
    5: {
        'libelle': 'Charges financieres',
        'comptes_a_inclure': ['66'],
        'comptes_a_exclure': [],
        },
    6: {
        'libelle': 'Charges exceptionnelles',
        'comptes_a_inclure': ['67'],
        'comptes_a_exclure': ['675', '676'],
    },
    7: {
        'libelle': 'Depenses directes d\'investissement',
        'comptes_a_inclure': ['20', '21', '23'],
        'comptes_a_exclure': ['204'],
    },
    8: {
        'libelle': 'Subventions d equipement versees',
        'comptes_a_inclure': ['204'],
        'comptes_a_exclure': [],
    },
    9: {
        'libelle': 'Prises de participation',
        'comptes_a_inclure': ['261', '271', '272', '25'],
        'comptes_a_exclure': [],
    },
    10: {
        'libelle': 'Prêts accordés',
        'comptes_a_inclure': ['26', '27'],
        'comptes_a_exclure': ['261', '271', '272', '25'],
    },
    11: {
        'libelle': 'Remboursement d\'emprunts et de dettes assimilées',
        'comptes_a_inclure': ['16'],
        'comptes_a_exclure': ['1688', '166'],
    },
}

LIBELLES_FONCTIONS = {
    0: 'Services généraux et opérations non ventilables',
    1: 'Sécurité et salubrité publiques',
    2: 'Enseignement – formation',
    3: 'Culture',
    4: 'Sport et jeunesse',
    5: 'Interventions sociales et santé',
    6: 'Famille',
    7: 'Logement',
    8: 'Aménagement et services urbains, environnement',
    9: 'Action économique',
}


def MODES_DE_CALCUL_DEPENSES(df):
    return [
        {
            'aggregats_id': [1, 2, 3, 4, 5, 6],
            'calcul': df['sd'] - df['sc'],
        },
        {
            'aggregats_id': [7, 8, 9],
            'calcul': (df['obnetdeb'] - df['obnetcre']) - (df['oobdeb'] - df['oobcre']),
        },
        {
            'aggregats_id': [10, 11],
            'calcul': df['obnetdeb'],
        },
    ]