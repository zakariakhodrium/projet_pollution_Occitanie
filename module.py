#Départements

import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

def plot_pie(department):
    """Cette fonction prend en argument un département de l'Occiatnie et renvoie un pie chart qui représente la part de chaque polluants au cours des cinq dernières années"""
    #Chargement du fichier CSV
    data = pd.read_csv("../data_visu/Mesure_annuelle_Region_Occitanie_Polluants_Principaux.csv")
    df = pd.DataFrame(data) # Création du Data Frame
    columns_to_drop = ['code_station', 'typologie', 'influence', 'id_poll_ue', 'unite', 'metrique', 'date_fin', 'statut_valid']
    df = df.drop(columns=columns_to_drop)

    df_department = df[df['nom_dept'] == department]

    df_department = df_department.dropna()
    df_department = df_department.groupby('nom_poll')['valeur'].sum().reset_index()

    name = df_department['nom_poll']
    value = df_department['valeur']

    plt.figure(figsize=(6, 6))
    plt.pie(value, labels=name, autopct='%1.1f%%', startangle=90, shadow=True)
    plt.axis('equal')
    plt.title(f"Répartition des polluants pour le département {department}")
    plt.show()




import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
def pollutants_evolution_dept_jour(csv, polluants, dept):
    """Cette fonction prend en argument un fichier CSV, la liste des polluants à afficher, ainsi que le département que l'on souhaite afficher et trace un graphique polair qui représente l'évolution de la concentration de chaque polluants choisis au cours de la journée"""
    df = pd.read_csv(csv)

    df['date_debut'] = pd.to_datetime(df['date_debut'], format='%Y/%m/%d %H:%M:%S%z')
    df = df.sort_values(by='date_debut')
    couleurs = ['blue', 'red', 'green', 'purple', 'orange', 'pink', 'brown']

    df_filtered = df[df['nom_poll'].isin(polluants)]

    df_city = df_filtered[df_filtered['nom_dept'] == dept]

    df_moyennes_city = df_city.groupby(['nom_poll', df_city['date_debut'].dt.weekday])['valeur'].mean().reset_index()
    df_moyennes_city.columns = ['nom_poll', 'jour', 'moyenne']


    df_moyennes_city['jour_complet'] = df_moyennes_city['jour'].apply(lambda x: ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'][x])

    fig = px.line_polar(
        df_moyennes_city,
        r="moyenne",
        theta="jour_complet",
        color="nom_poll",
        line_close=True,
        range_r=[0, df_moyennes_city['moyenne'].max() + 10],
        start_angle=0,
        template="seaborn",
        title=f"Évolution des polluants sur toute la semaine à {dept}",
        labels={"jour": "weekday"}
    )

    for i, row in df_moyennes_city.iterrows():
        jour_text = f"{row['jour_complet']}"
        fig.add_annotation(
            x=row['jour'] * (360 // 7),
            y=row['moyenne'],
            text=jour_text,
            showarrow=False,
            font=dict(size=10),
            textangle=0
        )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True),
            angularaxis=dict(
                tickmode='array',
                tickvals=list(range(7)),
                ticktext=["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
            )
        )
    )


    fig.show()

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
pd.options.mode.chained_assignment= None

def plot_pollutant_evolution_annuelle(data_file, department, polluants):
    """Cette fonction prend en argument le fichier CSV, le département et la liste des polluants à afficher et affiche l'évolution de la concentration par station de chaque polluants """
    # Charger les données
    df = pd.read_csv(data_file)
    df['valeur'].fillna(0, inplace=True)
    # Afficher la liste des polluants présents dans le DataFrame
    liste_polluants = df['nom_poll'].unique()

    # Boucle à travers les polluants pour créer les graphiques
    for polluant in polluants:
        # Filtrer les données pour le polluant et le département spécifiés
        filt = df[(df['nom_dept'] == department) & (df['nom_poll'] == polluant)]
        filt = filt.sort_values(by='date_debut')

        # Convertir la colonne de dates au format mois-année
        filt['date_debut'] = pd.to_datetime(filt['date_debut']).dt.to_period('M').astype(str)

        # Créer un graphique interactif avec Plotly Express
        fig = px.scatter(
            filt, x='date_debut', y='valeur',
            color='nom_station', size='valeur', hover_name='date_debut',
            title=f'Évolution de la pollution {polluant} dans le {department}',
            labels={'valeur': f'Valeur {polluant} (ug.m-3)', 'date_debut': 'Année'}
        )

        # Ajouter des lignes reliant les points pour chaque station
        for nom_station in filt['nom_station'].unique():
            trace_data = filt[filt['nom_station'] == nom_station]
            fig.add_trace(go.Scatter(
                x=trace_data['date_debut'],
                y=trace_data['valeur'],
                mode='lines',  # Ajout de ligne pour relier les points
                showlegend=False
            ))
        fig.show()

plot_pollutant_evolution_annuelle("../data_visu/Mesure_annuelle_Region_Occitanie_Polluants_Principaux.csv","GARD",['NO2', 'PM2.5', 'PM10', 'NOX', 'NO'])
# Villes

import numpy as np
def create_polar_plot(ville):
    # chargez csv
    df = pd.read_csv("../Mesure_30j.csv")
    # convert data
    df['date_debut'] = pd.to_datetime(df['date_debut'], format='%Y/%m/%d %H:%M:%S%z')
    # polluants
    polluants = ['NO2', 'PM2.5', 'PM10', 'NOX', 'NO']
    # Trier le DataFrame par ordre croissant de date
    df = df.sort_values(by='date_debut')
    df_filtered = df[df['nom_poll'].isin(polluants)]
    df_ville = df_filtered[df_filtered['nom_com']== ville]
    df_moyennes_ville = df_ville.groupby(['nom_poll', df_ville['date_debut'].dt.hour])['valeur'].mean().reset_index()
    df_moyennes_ville.columns = ['nom_poll', 'heure', 'moyenne']

    fig_pol =px.line_polar(
    df_moyennes_ville,
    r = 'moyenne' ,
    theta = df_moyennes_ville['heure']*(360//24),
    color ='nom_poll',
    title=f"Évolution des polluants sur toutes les heures à {ville}")

    fig_pol.update_polars(
    radialaxis=dict(
        visible=True,  # Set to False if you want to hide the radial axis
    ),
    angularaxis=dict(
        visible=True,  # Set to False if you want to hide the angular axis
        direction='clockwise',  # Set the direction of the angular axis
        period=360,   # Set the period of the angular axis
        tickvals=np.arange(0, 360, 15),
        ticktext=[str(hour % 24) for hour in range(24)],  # Specify tick values on the angular axis
    )
 )
    fig_pol.show()

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def afficher_evolution_pollution(nom_ville, chemin_fichier_csv, polluants):
    pd.options.mode.chained_assignment = None

    # Chargez le fichier CSV dans un DataFrame pandas
    df = pd.read_csv(chemin_fichier_csv)

    # Convertir la colonne 'date_debut' en type datetime
    df['date_debut'] = pd.to_datetime(df['date_debut'], format='%Y/%m/%d %H:%M:%S%z')

    # Trier le DataFrame par ordre croissant de date
    df = df.sort_values(by='date_debut')

    # Afficher la liste des polluants présents dans le DataFrame
    liste_polluants = df['nom_poll'].unique()

    # Boucle à travers les polluants pour créer les graphiques
    for polluant in polluants:
        # Regrouper les données de la ville spécifiée
        filt_data = df[(df['nom_com'] == nom_ville) & (df['nom_poll'] == polluant)]
        filt_data = filt_data.sort_values(by='date_debut')
        filt_data = filt_data.dropna()

        # Création d'un graphique
        fig = px.scatter(
            filt_data, x='date_debut', y='valeur',
            color='nom_station', hover_name='date_debut',
            title=f'Évolution de la pollution {polluant} à {nom_ville}',
            labels={'valeur': f'Valeur {polluant} (ug.m-3)', 'date_debut': 'Année'}
        )

        # Relier les points pour chaque station
        for nom_station in filt_data['nom_station'].unique():
            trace_data = filt_data[filt_data['nom_station'] == nom_station]
            fig.add_trace(go.Scatter(
                x=trace_data['date_debut'],
                y=trace_data['valeur'],
                mode='lines',
                showlegend=False
            ))
        fig.show()

import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

def pollutants_evolution_ville(csv, polluants, ville):
    df = pd.read_csv(csv)

    df['date_debut'] = pd.to_datetime(df['date_debut'], format='%Y/%m/%d %H:%M:%S%z')
    df = df.sort_values(by='date_debut')

    df_filtered = df[df['nom_poll'].isin(polluants)]

    df_city = df_filtered[df_filtered['nom_com'] == ville]

    df_moyennes_city = df_city.groupby(['nom_poll', df_city['date_debut'].dt.weekday])['valeur'].mean().reset_index()
    df_moyennes_city.columns = ['nom_poll', 'jour', 'moyenne']


    df_moyennes_city['jour_complet'] = df_moyennes_city['jour'].apply(lambda x: ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'][x])

    fig = px.line_polar(
        df_moyennes_city,
        r="moyenne",
        theta="jour_complet",
        color="nom_poll",
        line_close=True,
        range_r=[0, df_moyennes_city['moyenne'].max() + 10],
        start_angle=0,
        template="seaborn",
        title=f"Évolution des polluants sur toute la semaine à {ville}",
        labels={"jour": "weekday"}
    )

    for i, row in df_moyennes_city.iterrows():
        jour_text = f"{row['jour_complet']}"
        fig.add_annotation(
            x=row['jour'] * (360 // 7),
            y=row['moyenne'],
            text=jour_text,
            showarrow=False,
            font=dict(size=10),
            textangle=0
        )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True),
            angularaxis=dict(
                tickmode='array',
                tickvals=list(range(7)),
                ticktext=["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
            )
        )
    )


    fig.show()