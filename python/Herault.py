import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from pyproj import Proj, transform

url = "https://services9.arcgis.com/7Sr9Ek9c1QTKmbwr/arcgis/rest/services/mesures_occitanie_annuelle_poll_princ/FeatureServer/0/query?where=1%3D1&outFields=nom_dept,nom_com,insee_com,nom_station,nom_poll,valeur,unite,date_debut,x_l93,y_l93&outSR=4326&f=json"

# Extraction des données
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
    df_h = pd.DataFrame(records)
    df_h["valeur"].fillna(0, inplace=True)
    # Conversion des coordonnées Lambert 93 en latitude et longitude
    in_proj = Proj(init="epsg:2154")  # Lambert 93
    out_proj = Proj(init="epsg:4326")  # WGS84 (latitude, longitude)
    df_h["longitude"], df_h["latitude"] = transform(
        in_proj, out_proj, df_h["x_l93"].values, df_h["y_l93"].values
    )

    # Conversion de la colonne 'date_debut' qui est en millisecondes
    df_h["date_debut"] = pd.to_datetime(df_h["date_debut"], unit="ms")

# Liste des polluants à afficher
polluants = ["NO", "NOX", "O3", "PM10", "NO2"]
for polluant in polluants:
    # Regrouper les données de la ville de Montpellier
    filt_data = df_h[(df_h["nom_dept"] == "HERAULT") & (df_h["nom_poll"] == polluant)]
    filt_data = filt_data.sort_values(by="date_debut")


# Créer un graphique en ligne pour chaque polluant
for polluant in polluants:
    fig = px.scatter(
        df_h[df_h["nom_poll"] == polluant],
        x="date_debut",
        y="valeur",
        title=f"Évolution de {polluant} au fil du temps dans le département Hérault",
        labels={"valeur": "Concentration de Polluant", "date_debut": "Date"},
    )

    fig.show()
