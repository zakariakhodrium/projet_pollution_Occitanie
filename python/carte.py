import folium
import geopandas as gpd

# Lecture du fichier GeoJSON
donnees_geojson = gpd.read_file("Carte\Data_Carte\departements.geojson")
# Sélection des lignes avec code égal à 30 ou 34
codes_a_selectionner = [
    "11",
    "09",
    "12",
    "30",
    "31",
    "32",
    "34",
    "46",
    "48",
    "65",
    "66",
    "81",
    "82",
]
donnees_selectionnees = donnees_geojson[
    donnees_geojson["code"].isin(codes_a_selectionner)
]

# Affichage des lignes sélectionnées
print(donnees_selectionnees)

# Vérifier si des géométries ont été sélectionnées
if not donnees_selectionnees.empty:
    # Reprojeter les géométries dans un CRS projeté (par exemple, Web Mercator)
    donnees_selectionnees = donnees_selectionnees.to_crs(epsg=3857)

    # Créer une carte centrée sur la position moyenne des géométries sélectionnées
    latitude, longitude = (
        donnees_selectionnees.geometry.centroid.y.mean(),
        donnees_selectionnees.geometry.centroid.x.mean(),
    )
    ma_carte = folium.Map(location=[latitude, longitude], zoom_start=10)

    # Ajouter les géométries sélectionnées à la carte
    folium.GeoJson(donnees_selectionnees).add_to(ma_carte)

    # Enregistrer la carte au format HTML
    ma_carte.save("ma_carte.html")
    print("Carte générée avec succès.")
else:
    print("Aucune géométrie sélectionnée. Vérifiez vos codes de département.")


# Créer une carte centrée sur la position moyenne des géométries
"""latitude, longitude = donnees_selectionnees.geometry.centroid.y.mean(), donnees_selectionnees.geometry.centroid.x.mean()
ma_carte = folium.Map(location=[latitude, longitude], zoom_start=10)

# Ajouter les géométries à la carte
folium.GeoJson(donnees_selectionnees).add_to(ma_carte)

# Enregistrer la carte au format HTML
ma_carte.save("ma_carte.html")"""
ma_carte
