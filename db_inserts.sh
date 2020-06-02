rm app/data.db

echo "Inserting nomenclatures"
python3 db_insert/nomenclatures/run.py

echo "Inserting balances"
python3 db_insert/balances/run.py db_insert/balances/data/BalanceSPL_Fonction_2018_Dec2019.csv

echo "Inserting communes"
python3 db_insert/communes/run.py db_insert/communes/data/communes2020.csv db_insert/communes/data/Communes.csv