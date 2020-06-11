# installation des packages
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirement.txt

# Créer les tables et le repo des migrations (sqlite3 par défaut si la variable env DATABASE_URL n'est pas fixée)
flask db init
flask db migrate -m "Initialisation de la db"
flask db upgrade

# Créer les dossiers data et télécharger les données brutes
mkdir data/csv data/pickle
source data/insee.sh
source data/balances.sh