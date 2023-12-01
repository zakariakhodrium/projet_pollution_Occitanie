import pandas as pd
import requests
from pyproj import Proj, transform
from datetime import datetime, timedelta
import os

url='https://services9.arcgis.com/7Sr9Ek9c1QTKmbwr/arcgis/rest/services/mesures_occitanie_72h_poll_princ/FeatureServer/0/query?where=1%3D1&outFields=nom_dept,nom_station,code_station,nom_poll,valeur,unite,date_debut,x_l93,y_l93&outSR=4326&f=json'

response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    # Extraction des entités de la réponse JSON
    features = data.get('features', [])

    # Extraction des données pertinentes de chaque entité
    records = []
    for feature in features:
        attributes = feature.get('attributes', {})
        records.append(attributes)

    # Création d'un DataFrame
    df_data = pd.DataFrame(records)

    #Supprimer les lignes avec des données manquantes
    df_data=df_data.dropna()
    
    # Conversion des coordonnées Lambert 93 en latitude et longitude
    in_proj = Proj(init='epsg:2154')  # Lambert 93
    out_proj = Proj(init='epsg:4326')  # WGS84 (latitude, longitude)
    df_data['longitude'], df_data['latitude'] = transform(in_proj, out_proj, df_data['x_l93'].values, df_data['y_l93'].values)

    # Conversion de la colonne 'date_debut' qui est en millisecondes
    df_data['date_debut'] = pd.to_datetime(df_data['date_debut'], unit='ms')

    # Extraire les composants jour, mois, année et heure
    df_data['date_formatee'] = df_data['date_debut'].dt.strftime('%d/%m/%Y %H:%M')

    # Créer un DataFrame par département
    df_departements = {}
    for dept, group in df_data.groupby('nom_dept'):
        df_departements[dept] = group
    # Imprimer les DataFrames pour chaque département
    for dept, df_dept in df_departements.items():
        print(f"\nDataFrame pour le département {dept} :")
    pd.set_option('display.max_rows', None)  # Afficher toutes les lignes du DataFrame    
    print(df_departements['GERS'])
    
    # Regrouper les données par code_station dans chaque DataFrame de département
    df_departements_par_station = {}
    for dept, df_dept in df_departements.items():
        df_station = df_dept.groupby('code_station')
        df_departements_par_station[dept] = df_station      
    
    # Charger les données depuis le fichier CSV
    df_emplacements = pd.read_csv('c:/Users/aicha/OneDrive/Bureau/Projet pollution Occitanie/projet_pollution_Occitanie/data/code_station_emplacement.csv', encoding='latin-1',sep=';')

    # Créer un dictionnaire à partir du DataFrame
    dict_emplacements = df_emplacements.set_index('Code_Station')['Emplacement'].to_dict()
    
    # Ajouter une colonne 'emplacement' en utilisant le dictionnaire
    df_data['Emplacement'] = df_data['code_station'].map(dict_emplacements).fillna('Autre')

    # Créer un DataFrame par emplacement
    df_emplacements = {}
    for emplacement, group in df_data.groupby('Emplacement'):
        df_emplacements[emplacement] = group
        

    # Imprimer les DataFrames pour chaque emplacement
    for emplacement, df_emp in df_emplacements.items():
        print(f"\nDataFrame pour l'emplacement {emplacement} :")
        print(df_emp)
    
    # Répertoire où vous souhaitez enregistrer les fichiers CSV
    output_directory = 'c:/Users/aicha/OneDrive/Bureau/Projet pollution Occitanie/projet_pollution_Occitanie/data'

    # Enregistrez chaque département dans un fichier CSV
    for dept, df_dept in df_departements.items():
        # Construisez le chemin complet du fichier CSV
        csv_filename = os.path.join(output_directory, f"{dept}.csv")

        # Enregistrez le DataFrame au format CSV
        df_dept.to_csv(csv_filename, index=False)

        print(f"Fichier CSV enregistré pour le département {dept} : {csv_filename}")
    
    # Enregistrez un fichier CSV spécifique pour l'emplacement 'Toulouse'
    csv_filename_toulouse = os.path.join(output_directory, 'Toulouse.csv')
    df_emplacements['Toulouse'].to_csv(csv_filename_toulouse, index=False)
    print(f"Fichier CSV enregistré pour l'emplacement Toulouse : {csv_filename_toulouse}")

    # Enregistrez un fichier CSV spécifique pour l'emplacement 'Montpellier'
    csv_filename_montpellier = os.path.join(output_directory, 'Montpellier.csv')
    df_emplacements['Montpellier'].to_csv(csv_filename_montpellier, index=False)
    print(f"Fichier CSV enregistré pour l'emplacement Montpellier : {csv_filename_montpellier}")
        




