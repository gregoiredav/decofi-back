# ***** En construction *****

## API

L'API offre pour l'instant les ressources suivantes:

#### - Recherche de code insee par nom de commune

Exemple: communes contenant les lettres "Toulo", classées par ordre de population (max 100 résultats).
`http://3.122.51.179/communes?inputValue=Toulo`

#### - Requête des identifiants de budgets et dese aggrégats de dépenses par collectivite

Exemple: requête du budget de la commune avec code insee 31555 (Toulouse).
`http://3.122.51.179/collectivites/`

#### - Requête du détail des balances comptables pour un exercice budgétaire

`http://3.122.51.179/collectivites/<budget_id>`

## Data processing

Le dossier db_inserts contient les scripts qui créent la base de donnée de l'API

#### Nomenclatures

Le script initie les bases de données et crée les tables contenant les libellés des fonctions et des aggrégats de dépense.

`python3 db_inserts/nomenclatures/run.py`

#### Communes
Le script prend comme argument (dans l'ordre):
- la liste des communes ([source INSEE](https://www.insee.fr/fr/information/4316069))
- la population des communes ([source INSEE](https://www.insee.fr/fr/statistiques/4265429?sommaire=4265511))

`python3 db_inserts/communes/run.py <fichier communes> <fichier population>`

#### Balances comptables
Le script processe les balances des collectivités ([Source data.gouv](https://www.data.gouv.fr/fr/datasets/balances-comptables-des-collectivites-et-des-etablissements-publics-locaux-avec-la-presentation-croisee-nature-fonction-2017/)), identifie les dépenses et les aggrège par commune et par exercice budgétaire.

`python3 db_inserts/balances/run.py <fichier balances>`

