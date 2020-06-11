# ***** En construction *****

L'objectif de cette repo est de faciliter l'accès aux données des balances comptables des collectivités territoriales (seulement disponible sous force de CSV gigantesques), 
et graduellement d'y ajouter des ressources de nomenclature afin d'en faciliter la compréhension. 

Pour l'instant, 2 abstractions de haut-niveau sont proposée:
- la fonction (code fonction et libellé)
- des aggrégats de compte correspondant à des types de dépenses

Les instructions ci-dessous concernent:
- l'utilisation de l'API existante
- comment utiliser le code pour recréer cette API

## Tester l'API

L'API offre pour l'instant les ressources suivantes:

#### Pour une collectivité, requête des identifiants de budgets et des aggrégats de dépenses pour ces budgets

Exemple: requête du budget de la commune avec code insee 01034 (commune de Belley).

`http://3.122.51.179/collectivites/01034`

#### Pour un exercice budgétaire, requête du détail des balances comptables

Exemple: requête du détail des balances comptables pour l'exercice 2018 à Belley

`http://3.122.51.179/budgets/01034/2018`

## Utiliser le code

Cloner le repo:

`git clone https://github.com/gregoiredav/decofi-back.git`

Une fois le repo cloné, un script permet de créer la base de donnée et de télécharger les données brutes:

`source bootstrap.sh`

Le dossier `manage_db` contient ensuite des ressources pour mettre en forme les données, et les insérer dans la base
de donnée via des endpoints de type `POST` ou `PUT`. Les étapes pour créer une base de donnée en ordre de marche seraient:

(1) Remplir les tables de type nomenclature.

`python3 manage_db/nomenclatures/create.py`

(2) Traiter les CSV de l'insee pour insérer les collectivités dans la base de donnée (via le webserver, qui doit être up)

`python3 manage_db/collectivites/post.py data/csv/insee_codes.csv data/csv/insee_population.csv <adresse du webserver>`

(3) Nettoyer le csv des balances comptables et sauver les données préparées sous format pickle (example pour les balances 2016)

`python3 manage_db/balances/process_csv.py data/csv/BalanceSPL_Fonction_2016_Juin2019.csv balances_2016.pickle`

(4) Traiter un fichier .pickle de balances, et insérer les données dans la base de donnée (via le webserver) 

`python3 manage_db/balances/post.py data/pickle/balances_2018.pickle <adresse du webserver>`
