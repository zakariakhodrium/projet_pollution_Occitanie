import pandas as pd
import requests
import geopandas as gpd


url = "https://services9.arcgis.com/7Sr9Ek9c1QTKmbwr/arcgis/rest/services/Indice_quotidien_de_qualité_de_l’air_pour_les_collectivités_territoriales_en_Occitanie/FeatureServer/0/query?where=1%3D1&outFields=date_ech,code_qual,lib_qual,code_zone,code_no2,code_so2,code_o3,code_pm10,code_pm25,x_wgs84,y_wgs84,x_reg,y_reg,coul_qual&outSR=4326&f=json"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    # Extraction des entités de la réponse JSON
    features = data.get("features", [])

    # Extraction des données pertinentes de chaque entité
    records = []
    for feature in features:
        attributes = feature.get("attributes", {})
        records.append(attributes)

    # Création d'un DataFrame
    df_data = pd.DataFrame(records)

    # Supprimer les lignes avec des données manquantes
    df_data = df_data.dropna()

    # Supposons que vous avez une colonne 'date_debut' avec des durées en millisecondes
    df_data["date_ech"] = pd.to_datetime(df_data["date_ech"], unit="ms")
    # Extraire les composants jour, mois, année et heure
    df_data["date_formatee"] = df_data["date_ech"].dt.strftime("%d/%m/%Y")

    print(df_data)
    # c:/Users/aicha/OneDrive/Bureau/Projet pollution Occitanie/projet_pollution_Occitanie/data
    # Lecture d'un csv contenant tout les codes zone associées aux 13 départements
    dept = pd.read_excel("data/dept.xlsx")

    # Get  13 clean (i.e doesn't contain empty values) lists that contains the codes of zones of each departments from our data frame "dept"
    dept_lists = [dept[col].dropna().tolist() for col in dept.columns]

    # From the "dept" df get the names of each department
    dept_names = dept.columns.to_list()

    # Create a dictionary that assign each dept to it's codes of zone
    data2 = dict(zip(dept_names, dept_lists))

    # Ariège
    df_Ariège = df_data[df_data["code_zone"].isin(data2["Ariège"])]
    # Aude
    df_Aude = df_data[df_data["code_zone"].isin(data2["Aude"])]
    # Averyron
    df_Averyron = df_data[df_data["code_zone"].isin(data2["Averyron"])]
    # Gard
    df_Gard = df_data[df_data["code_zone"].isin(data2["Gard"])]
    # Gers
    df_Gers = df_data[df_data["code_zone"].isin(data2["Gers"])]
    # Hautes_Pyrénées
    df_Hautes_Pyrénées = df_data[df_data["code_zone"].isin(data2["Hautes-Pyrénées"])]
    # Hérlaut
    df_Hérlaut = df_data[df_data["code_zone"].isin(data2["Hérlaut"])]
    # Lot
    df_Lot = df_data[df_data["code_zone"].isin(data2["Lot"])]
    # Lozère
    df_Lozère = df_data[df_data["code_zone"].isin(data2["Lozère"])]
    # Pyrénées_Orientales
    df_Pyrénées_Orientales = df_data[
        df_data["code_zone"].isin(data2["Pyrénées-Orientales"])
    ]
    # Tarn
    df_Tarn = df_data[df_data["code_zone"].isin(data2["Tarn"])]
    # Tarn_garonne
    df_Tarn_garonne = df_data[df_data["code_zone"].isin(data2["Tarn-et garonne"])]
    # Haute_Garonne
    df_Haute_Garonne = df_data[df_data["code_zone"].isin(data2["Haute-Garonne"])]

    print(df_Averyron)
