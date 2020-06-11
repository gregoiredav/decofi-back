# Fichiers des balances comptables avec présentation croisée nature / fonction disponibles sur data.gouv

# Balances 2018
# https://www.data.gouv.fr/fr/datasets/balances-comptables-des-collectivites-et-des-etablissements-publics-locaux-avec-la-presentation-croisee-nature-fonction-2018/
curl -o balances.zip https://data.economie.gouv.fr/api/datasets/1.0/balances-comptables-des-collectivites-et-des-etablissements-publics-locaux-avec0/attachments/balancespl_fonction_2018_dec2019_zip
unzip balances.zip -d data/csv
rm balances.zip

# Balances 2017
# https://www.data.gouv.fr/fr/datasets/balances-comptables-des-collectivites-et-des-etablissements-publics-locaux-avec-la-presentation-croisee-nature-fonction-2017/
curl -o balances.zip https://data.economie.gouv.fr/api/datasets/1.0/balances-comptables-des-collectivites-et-des-etablissements-publics-locaux-avec-/attachments/balancespl_fonction_2017_dec2018_zip
unzip balances.zip -d data/csv
rm balances.zip

# Balances 2016
# https://www.data.gouv.fr/fr/datasets/balances-comptables-des-collectivites-et-des-etablissements-publics-locaux-avec-la-presentation-croisee-nature-fonction-2016/
curl -o balances.zip https://data.economie.gouv.fr/api/datasets/1.0/balances-comptables-des-collectivites-et-des-etablissements-publics-locaux-avec1/attachments/balancespl_fonction_2016_juin2019_zip
unzip balances.zip -d data/csv
rm balances.zip
