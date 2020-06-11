# Fichier populations
# Plus de renseignements: https://www.insee.fr/fr/statistiques/4265429?sommaire=4265511
curl -o insee_population.zip https://www.insee.fr/fr/statistiques/fichier/4265429/ensemble.zip
unzip insee_population.zip -d insee_population
mv insee_population/Communes.csv data/csv/insee_population.csv
rm -r insee_population/ insee_population.zip

# Fichier code géographique nom et catégories
# Plus de renseignements: https://www.insee.fr/fr/information/4316069
curl -o insee_codes.zip https://www.insee.fr/fr/statistiques/fichier/4316069/communes2020-csv.zip
unzip insee_codes.zip
mv communes2020.csv data/csv/insee_codes.csv
rm insee_codes.zip