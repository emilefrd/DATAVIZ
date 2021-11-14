from plotly.express import colors
import streamlit as st
import pandas as pd
import plotly_express as px
import plotly.graph_objects as go
import logging
import time
import matplotlib.pyplot as plt
import seaborn as sns

from functools import wraps
import logging


#LOGGER
logger = logging.getLogger(__name__)

logger.setLevel("INFO")
handler = logging.FileHandler(filename="log.txt", mode="a")
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s -- %(message)s"))
logger.addHandler(handler)

logging.info('\nNew Execution at :', time.time(), "\n")

def timed(func):
    """This decorator prints the execution time for the decorated function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.info("{} ran in {}s".format(func.__name__, round(end - start, 2)))
        return result

    return wrapper


##############################################################################
#Generals informations about my pages
PAGE_CONFIG = {"page_title" : "Dashbord immobilier", "page_icon":"./images/index.png", "layout": "wide", "initial_sidebar_state" : 'collapsed'}
st.set_page_config(**PAGE_CONFIG)

st.sidebar.success("Liens externes")

st.markdown("<h1 style='text-align:center'>Dashboard sur l'immobilier en France de 2017 à 2020</h1>", unsafe_allow_html=True)

##############################################################################
##Import my clean csv
#filepath
file_clean_data2017 = './CSVclean/clean_2017.csv'
file_clean_data2018 = './CSVclean/clean_2018.csv'
file_clean_data2019 = './CSVclean/clean_2019.csv'
file_clean_data2020 = './CSVclean/clean_2020.csv'

#import csv
@st.cache(allow_output_mutation=True)
def import_clean_csv(filepath):
    df = pd.read_csv(filepath, delimiter = ',')
    return df

#dataframe for maps
@st.cache(allow_output_mutation=True)
def place_on_map(df):
    df = df[['latitude','longitude']]
    return df

#############################################################################
##Function for print my analysys
#Allow to show 5 firts lines of dataframes
def perceive(df):
    col1, col2, col3 = st.columns(3)
    with col1:
        pass
    with col2: 
        yes = st.checkbox("Afficher une partie du dataset à étudier" )
        if yes:
            st.write(df.head())
    with col3:
        pass
    


#Chart of type local in function of years
def chart_type_local_by_years(df,year):
    colors = ['#ffbdbd', '#ff8787', '#ff3838']
    st.markdown(f"<h1 style='text-align:center'>Types de local les plus présents en {year} :</h1>", unsafe_allow_html=True)
    name=['Maison',"Appartement","Local industriel. commercial ou assimilé"]
    local_type = df['type_local'].value_counts()
    fig = go.Figure(data=[go.Pie(labels=name, values=local_type, hole=.3)])
    fig.update_traces(textfont_size=20, marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    return st.plotly_chart(fig)

#Chart of nature mutation in function of years
def chart_nature_mutation_by_years(df,year):
    colors = ['#ffbdbd', '#ff8787', '#ff3838']
    st.markdown(f"<h1 style='text-align:center'>Nature mutation les plus présentes en {year} :</h1>", unsafe_allow_html=True)
    name=['Vente', "Vente en l'état futur d'achèvement" ,'Adjudication' ,'Echange','Vente terrain à bâtir' ,'Expropriation']
    local_type = df['nature_mutation'].value_counts()
    fig = go.Figure(data=[go.Pie(labels=name, values=local_type, hole=.3)])
    fig.update_traces(textfont_size=20, marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    return st.plotly_chart(fig)

#means price of houses
def mean_biens(df,biens):
        df_bien = df[df['type_local'] == biens ]
        mean_price_bien = round(df_bien['valeur_fonciere'].mean())
        return mean_price_bien

# print mean price by type
def print_mean_bien(df):
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.markdown(f"<h1 style='text-align: center; color:black;'>Prix moyens en fonction du type local</h1>", unsafe_allow_html=True)
    Maison, Appartement, Local = st.columns(3)
    with Maison :
        st.image('./images/MAISON.png', width= 200)
        st.markdown("**Prix moyen d'une Maison :**")
        st.markdown(f"<h1 style='text-align: center; color:black;'>{mean_biens(df,'Maison')}</h1>", unsafe_allow_html=True)

    with Appartement :
        st.image('./images/appartement.png',width= 200)
        st.markdown("**Prix moyen d'un Appartement :**")
        st.markdown(f"<h1 style='text-align: center; color:black;'>{mean_biens(df,'Appartement')}</h1>", unsafe_allow_html=True)

    with Local :
        st.image('./images/entreprise.png',width= 200)
        st.markdown("**Prix moyen d'un Local :**")
        st.markdown(f"<h1 style='text-align: center; color:black;'>{mean_biens(df,'Local industriel. commercial ou assimilé')}</h1>", unsafe_allow_html=True)


#mean price of m2 by houses
def mean_biens_m2(df,biens):
        df['mean_price_m2'] = df['valeur_fonciere'] / df['surface_reelle_bati']
        df_bien = df[df['type_local'] == biens ]
        mean_price_bien_m2 = round(df_bien['mean_price_m2'].mean())
        return mean_price_bien_m2

#print mean price by m2
def print_mean_bien_m2(df):
    Maison, Appartement, Local = st.columns(3)
    with Maison :
        st.markdown("**Prix moyen au M2 d'une Maison :**")
        st.markdown(f"<h1 style='text-align: center; color:grey;'>{mean_biens_m2(df,'Maison')}</h1>", unsafe_allow_html=True)
    with Appartement :
        st.markdown("**Prix moyen au M2 d'un Appartement :**")
        st.markdown(f"<h1 style='text-align: center; color:grey;'>{mean_biens_m2(df,'Appartement')}</h1>", unsafe_allow_html=True)

    with Local :
        st.markdown("**Prix moyen au M2 d'un Local:**")
        st.markdown(f"<h1 style='text-align: center; color:grey;'>{mean_biens_m2(df,'Local industriel. commercial ou assimilé')}</h1>", unsafe_allow_html=True)

#evolution fonction for compare year with another year
def evolution(df1,df0,type):
    n0 = mean_biens(df0,type)
    n1 = mean_biens(df1,type)
    percent = 100*((n1 - n0)/n0)
    percent = round(percent,3)
    return percent

#print the evolution
def print_evolution_year(df1,df0):
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.markdown(f"<h1 style='text-align: center; color:black;'>Evolution des valeurs foncieres par rapport à l'année précédente</h1>", unsafe_allow_html=True)
    Maison, Appartement, Local = st.columns(3)
    with Maison :
        st.markdown("**Maison :**")
        if evolution(df1,df0,'Maison') > 0:
            st.markdown(f"<h1 style='text-align: center; color:red;'>{evolution(df1,df0,'Maison')}%</h1>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h1 style='text-align: center; color:green;'>{evolution(df1,df0,'Maison')}%</h1>", unsafe_allow_html=True)
    with Appartement :
        st.markdown("**Appartement :**")
        if evolution(df1,df0,'Appartement') > 0:
            st.markdown(f"<h1 style='text-align: center; color:red;'>{evolution(df1,df0,'Appartement')}%</h1>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h1 style='text-align: center; color:green;'>{evolution(df1,df0,'Appartement')}%</h1>", unsafe_allow_html=True)

    with Local :
        st.markdown("**Local:**")
        if evolution(df1,df0,'Local industriel. commercial ou assimilé') > 0:
            st.markdown(f"<h1 style='text-align: center; color:red;'>{evolution(df1,df0,'Local industriel. commercial ou assimilé')}%</h1>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h1 style='text-align: center; color:green;'>{evolution(df1,df0,'Local industriel. commercial ou assimilé')}%</h1>", unsafe_allow_html=True)

#evolution month
def evolution_month(df,month1,month2):
    df['month'] = pd.DatetimeIndex(df['date_mutation']).month
    df1 =  df[df['month']== month1]
    df2 =  df[df['month']== month2]
    mean_price_bien_M1 = round(df1['valeur_fonciere'].mean())
    mean_price_bien_M2 = round(df2['valeur_fonciere'].mean())
    percent = 100 *((mean_price_bien_M2 - mean_price_bien_M1 )/mean_price_bien_M1)
    percent = round(percent,3)
    return percent

#print evolution month
def print_evolution_month(df):
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.markdown(f"<h1 style='text-align: center; color:black;'>Evolution des valeurs foncieres par rapport au mois précédents</h1>", unsafe_allow_html=True)
    Janvier, Fevrier ,Mars, Avril, Mai, Juin = st.columns(6)
    Juillet, Aout, Septembre, Octobre, Novembre, Décembre = st.columns(6)
    with Janvier :
        st.markdown("**Janvier**")
        if evolution_month(df,1,2)>0:
            st.markdown(f"<h1 style='text-align: center; color:red;'>{evolution_month(df,1,2)}%</h1>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h1 style='text-align: center; color:green;'>{evolution_month(df,1,2)}%</h1>", unsafe_allow_html=True)
    with Fevrier :
        st.markdown("**Fevrier**")
        if evolution_month(df,1,2)>0:
            st.markdown(f"<h1 style='text-align: center; color:red;'>{evolution_month(df,1,2)}%</h1>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h1 style='text-align: center; color:green;'>{evolution_month(df,1,2)}%</h1>", unsafe_allow_html=True)
    with Mars :
        st.markdown("**Mars**")
        if evolution_month(df,2,3)>0:
            st.markdown(f"<h1 style='text-align: center; color:red;'>{evolution_month(df,2,3)}%</h1>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h1 style='text-align: center; color:green;'>{evolution_month(df,2,3)}%</h1>", unsafe_allow_html=True)
    with Avril:
        st.markdown("**Avril**")
        if evolution_month(df,3,4)>0:
            st.markdown(f"<h1 style='text-align: center; color:red;'>{evolution_month(df,3,4)}%</h1>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h1 style='text-align: center; color:green;'>{evolution_month(df,3,4)}%</h1>", unsafe_allow_html=True)
    with Mai:
        st.markdown("**Mai**")
        if evolution_month(df,4,5)>0:
            st.markdown(f"<h1 style='text-align: center; color:red;'>{evolution_month(df,4,5)}%</h1>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h1 style='text-align: center; color:green;'>{evolution_month(df,4,5)}%</h1>", unsafe_allow_html=True)
    with Juin:
        st.markdown("**Juin**")
        if evolution_month(df,5,6)>0:
            st.markdown(f"<h1 style='text-align: center; color:red;'>{evolution_month(df,5,6)}%</h1>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h1 style='text-align: center; color:green;'>{evolution_month(df,5,6)}%</h1>", unsafe_allow_html=True)
    with Juillet:
        st.markdown("**Juillet**")
        if evolution_month(df,6,7)>0:
            st.markdown(f"<h1 style='text-align: center; color:red;'>{evolution_month(df,6,7)}%</h1>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h1 style='text-align: center; color:green;'>{evolution_month(df,6,7)}%</h1>", unsafe_allow_html=True)
    with Aout:
        st.markdown("**Aout**")
        if evolution_month(df,7,8)>0:
            st.markdown(f"<h1 style='text-align: center; color:red;'>{evolution_month(df,7,8)}%</h1>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h1 style='text-align: center; color:green;'>{evolution_month(df,7,8)}%</h1>", unsafe_allow_html=True)
    with Septembre:
        st.markdown("**Septembre**")
        if evolution_month(df,8,9)>0:
            st.markdown(f"<h1 style='text-align: center; color:red;'>{evolution_month(df,8,9)}%</h1>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h1 style='text-align: center; color:green;'>{evolution_month(df,8,9)}%</h1>", unsafe_allow_html=True)
    with Octobre:
        st.markdown("**Octobre**")
        if evolution_month(df,9,10)>0:
            st.markdown(f"<h1 style='text-align: center; color:red;'>{evolution_month(df,9,10)}%</h1>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h1 style='text-align: center; color:green;'>{evolution_month(df,9,10)}%</h1>", unsafe_allow_html=True)
    with Novembre:
        st.markdown("**Novembre**")
        if evolution_month(df,10,11)>0:
            st.markdown(f"<h1 style='text-align: center; color:red;'>{evolution_month(df,10,11)}%</h1>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h1 style='text-align: center; color:green;'>{evolution_month(df,10,11)}%</h1>", unsafe_allow_html=True)
    with Décembre:
        st.markdown("**Decembre**")
        if evolution_month(df,11,12)>0:
            st.markdown(f"<h1 style='text-align: center; color:red;'>{evolution_month(df,11,12)}%</h1>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h1 style='text-align: center; color:green;'>{evolution_month(df,11,12)}%</h1>", unsafe_allow_html=True)
    st.write('')
    st.write('')
    st.write('')
    st.write('')



#Function for see values in maps
def mapping(df,year):
    st.markdown(f"<h1 style='text-align:center'>Voici les biens immobiliers présents dans la région sélectionées pour l'année {year} :</h1>", unsafe_allow_html=True)
    choice = st.selectbox('De quelle region de métropole française voulez vous etudiez le marché ?', (
        'Auvergne-Rhône-Alpes',
        'Bourgogne-Franche-Comté',
        'Bretagne',
        'Centre-Val de Loire',
        'Corse',
        'Grand Est',
        'Hauts-de-France',
        'Île-de-France',
        'Normandie',
        'Nouvelle-Aquitaine',
        'Occitanie',
        'Pays de la Loire',
        "Provence-Alpes-Côte d'Azur"))

    if choice == ('Auvergne-Rhône-Alpes') :
        map1 = px.density_mapbox(place_on_map(df), lat='latitude', lon='longitude', radius=1,center=dict(lat=45.763420, lon=4.834277), zoom=7,width= 1200,mapbox_style="open-street-map", template='seaborn')
        st.plotly_chart(map1)

    if choice == ('Bourgogne-Franche-Comté'):
        map2 = px.density_mapbox(place_on_map(df), lat='latitude', lon='longitude', radius=1,center=dict(lat= 47.596, lon=46.997), zoom=7,width= 1200,mapbox_style="open-street-map", template='seaborn')
        st.plotly_chart(map2)    

    if choice == ('Bretagne'):
        map3 = px.density_mapbox(place_on_map(df), lat='latitude', lon='longitude', radius=1,center=dict(lat=48.185, lon=-2.774), zoom=7,width= 1200,mapbox_style="open-street-map", template='seaborn')
        st.plotly_chart(map3)

    if choice == ('Centre-Val de Loire'):
        map4 = px.density_mapbox(place_on_map(df), lat='latitude', lon='longitude', radius=1,center=dict(lat=47.7515, lon=1.675), zoom=7,width= 1200,mapbox_style="open-street-map", template='seaborn')
        st.plotly_chart(map4)

    if choice == ('Corse'):
        map5 = px.density_mapbox(place_on_map(df), lat='latitude', lon='longitude', radius=1,center=dict(lat=42.039604, lon=9.012893), zoom=7,width= 1200,mapbox_style="open-street-map", template='seaborn')
        st.plotly_chart(map5)

    if choice == ('Grand Est'):
        map6 = px.density_mapbox(place_on_map(df), lat='latitude', lon='longitude', radius=1,center=dict(lat=48.580002, lon=7.750000), zoom=7,width= 1200,mapbox_style="open-street-map", template='seaborn')
        st.plotly_chart(map6)
    if choice == ('Hauts-de-France'):
        map7 = px.density_mapbox(place_on_map(df), lat='latitude', lon='longitude', radius=1,center=dict(lat=50.629250, lon=3.057256), zoom=7,width= 1200,mapbox_style="open-street-map", template='seaborn')
        st.plotly_chart(map7)

    if choice == ('Île-de-France'):
        map8 = px.density_mapbox(place_on_map(df), lat='latitude', lon='longitude', radius=1,center=dict(lat=48.856614, lon=2.3522219), zoom=7,width= 1200,mapbox_style="open-street-map", template='seaborn')
        st.plotly_chart(map8)

    if choice == ('Normandie'):
        map9 = px.density_mapbox(place_on_map(df), lat='latitude', lon='longitude', radius=1,center=dict(lat=49.180000, lon=-0.370000), zoom=7,width= 1200,mapbox_style="open-street-map", template='seaborn')
        st.plotly_chart(map9)

    if choice == ('Nouvelle-Aquitaine'):
        map10 = px.density_mapbox(place_on_map(df), lat='latitude', lon='longitude', radius=1,center=dict(lat=43.480000, lon=-1.560000), zoom=7,width= 1200,mapbox_style="open-street-map", template='seaborn')
        st.plotly_chart(map10)

    if choice == ('Occitanie'):
        map11 = px.density_mapbox(place_on_map(df), lat='latitude', lon='longitude', radius=1,center=dict(lat=43.604500, lon=1.444000), zoom=7,width= 1200,mapbox_style="open-street-map", template='seaborn')
        st.plotly_chart(map11)

    if choice == ('Pays de la Loire'):
        map12 = px.density_mapbox(place_on_map(df), lat='latitude', lon='longitude', radius=1,center=dict(lat=47.168900, lon=-1.469700), zoom=7,width= 1200,mapbox_style="open-street-map", template='seaborn')
        st.plotly_chart(map12)

    if choice == ("Provence-Alpes-Côte d'Azur"):
        map13 = px.density_mapbox(place_on_map(df), lat='latitude', lon='longitude', radius=1,center=dict(lat=43.9351691, lon=6.0679194), zoom=7,width= 1200,mapbox_style="open-street-map", template='seaborn')
        st.plotly_chart(map13)

#Function for print my histogram
def plot_dist(df, col, color):
        fig_graph = (go.Histogram(x = df[col], y = df["valeur_fonciere"], name = col, marker_color=color )) 
        fig_layout = dict(xaxis = dict(title = col, range=[0, df[col].quantile(.95)]),yaxis = dict(title = 'volume'),autosize=False, paper_bgcolor="#F8F8F8", )
        fig = dict(data=fig_graph,layout=fig_layout)
        st.plotly_chart(fig)

#Number of cities
def number_of_cities (df):
    st.markdown(f"<h1 style='text-align: center; color:black;'>Fréquence d'apparition d'une commune dans le dataset</h1>", unsafe_allow_html=True)
    n = st.slider('Nombre de communes :', 1, 30,5)
    st.header('TOP '+str(n)+ ' des communes les plus représentées')
    values = df['nom_commune'].value_counts().head(n)
    #values = values.sort_values(by=['nom_commune'])
    st.bar_chart(values)


#function for count rows
def count_rows(rows): 
    return len(rows)

#heatmap
def number_main_room_real_surface(df):
        df = df.groupby(['nombre_pieces_principales','surface_reelle_bati']).apply(count_rows).unstack()
        fig, ax = plt.subplots(figsize=(11,9))
        ax = sns.heatmap(df)
        return st.write(fig)

# hist 1 _ number of main rooms in function of type local
def number_of_piece_type_local(df):
    st.markdown(f"<h1 style='text-align: center; color:black;'>Nombre de pieces principales en fonction du type local</h1>", unsafe_allow_html=True)
    df = df[['type_local','nombre_pieces_principales']]
    fig = px.scatter(df, x='type_local', y='nombre_pieces_principales')
    st.write(fig)

# hist 2 _ number of main rooms in function of nature mutation
def number_of_piece_nature_mutation(df):
    st.markdown(f"<h1 style='text-align: center; color:black;'>Nombre de pieces principales en fonction de la nature de la mutation</h1>", unsafe_allow_html=True)
    df = df[['nature_mutation','nombre_pieces_principales']]
    fig = px.scatter(df, x='nature_mutation', y='nombre_pieces_principales')
    st.write(fig)

#hist3 _ land surface in funciton of nature mutation
def surface_land_valeur_fonciere(df):
    st.markdown(f"<h1 style='text-align: center; color:black;'>Surface du terrain en fonction de la valeur fonciere</h1>", unsafe_allow_html=True)
    figuree = px.scatter(twenty, x = twenty['valeur_fonciere'], y = twenty['surface_terrain'], \
                                    color_continuous_scale=px.colors.sequential.Viridis)
    return st.plotly_chart(figuree)
    
# hist 4 _ surface land in function of code departement 
def surface_land_code_departement(df):
    st.markdown(f"<h1 style='text-align: center; color:black;'>Surface du terrain en fonction du code de département</h1>", unsafe_allow_html=True)
    df = df[['code_departement','surface_terrain']]
    fig = px.scatter(df, x='code_departement', y='surface_terrain')
    st.write(fig)

#create spaeces and pictures into presentation
def spaces(link):
    return st.image(link, width= 1200)




###My rapport
twenty = import_clean_csv(file_clean_data2020)
nineteen = import_clean_csv(file_clean_data2019)
eighteen = import_clean_csv(file_clean_data2018)
seventeen = import_clean_csv(file_clean_data2017)


###############################   MAIN FUNCTION ############################################################
@timed
def body():
    st.sidebar.image('https://static.thenounproject.com/png/1876233-200.png')
    st.sidebar.write('Ci dessous : videos utiles à la compréhension du marché')
    st.sidebar.write('')
    st.sidebar.video('https://www.youtube.com/watch?v=3sCnwzWuJuo')
    st.sidebar.video('https://www.youtube.com/watch?v=IrSjltcFWiU')
    st.sidebar.write('')
    st.sidebar.write('')
    st.sidebar.text_input("Ajouter vos coordonées pour etre recontacté(e) par l'un / l'une de nos conseillers/ conseilleres",
    ("Telephone")
)
    spaces('./presentation/dataset.png')
    choice = st.radio("Choisir votre dataset : ",('2020','2019','2018','2017'))
    ##2020
    if choice == '2020' :
        perceive(twenty)
        spaces('./presentation/prix_moyens.png')
        print_mean_bien(twenty)
        print_mean_bien_m2(twenty)
        print_evolution_year(twenty,nineteen)
        print_evolution_month(twenty)
        spaces('./presentation/diagramme_circulaire.png')
        Type_local, Nature_mutation = st.columns(2)
        with Type_local:
            chart_type_local_by_years(twenty,2020)
        with Nature_mutation:
            chart_nature_mutation_by_years(twenty,2020)
        spaces('./presentation/carte.png')
        mapping(twenty,2020)
        spaces('./presentation/histo.png')
        st.write('**Valeur fonciere en fonction de la surface réeele du batiment**')
        plot_dist(twenty,'surface_reelle_bati','#0a0403')
        st.write('**Valeur fonciere en fonction du nombre de piece principale**')
        plot_dist(twenty,'nombre_pieces_principales','#0a0403')
        st.write('**Valeur fonciere en fonction de la surface réeele du terrain**')
        plot_dist(twenty,'surface_terrain','#0a0403')
        spaces('./presentation/communes.png')
        number_of_cities(twenty)
        spaces('./presentation/heatmap.png')
        Afficher = st.button('Afficher la Heatmap')
        if Afficher :
            number_main_room_real_surface(twenty)
        spaces('./presentation/nuagedepoints.png')
        typelocal, naturemutation = st.columns(2)
        with typelocal :
            number_of_piece_type_local(twenty)
        with naturemutation :
            number_of_piece_nature_mutation(twenty)
        valeurfonciere , codedep = st.columns(2)
        with valeurfonciere:
            surface_land_valeur_fonciere(twenty)
        with codedep:
            surface_land_code_departement(twenty)
    ##2019
    if choice == '2019' :
        perceive(nineteen)
        spaces('./presentation/prix_moyens.png')
        print_mean_bien(nineteen)
        print_mean_bien_m2(nineteen)
        print_evolution_year(nineteen,eighteen)
        print_evolution_month(nineteen)
        spaces('./presentation/diagramme_circulaire.png')
        Type_local, Nature_mutation = st.columns(2)
        with Type_local:
            chart_type_local_by_years(nineteen,2019)
        with Nature_mutation:
            chart_nature_mutation_by_years(nineteen,2019)
        spaces('./presentation/carte.png')
        mapping(nineteen,2019)
        spaces('./presentation/histo.png')
        st.write('**Valeur fonciere en fonction de la surface réeele du batiment**')
        plot_dist(nineteen,'surface_reelle_bati','#0a0403')
        st.write('**Valeur fonciere en fonction du nombre de piece principale**')
        plot_dist(nineteen,'nombre_pieces_principales','#0a0403')
        st.write('**Valeur fonciere en fonction de la surface réeele du terrain**')
        plot_dist(nineteen,'surface_terrain','#0a0403')
        spaces('./presentation/communes.png')
        number_of_cities(nineteen)
        spaces('./presentation/heatmap.png')
        Afficher = st.button('Afficher la Heatmap')
        if Afficher :
            number_main_room_real_surface(nineteen)
        spaces('./presentation/nuagedepoints.png')
        typelocal, naturemutation = st.columns(2)
        with typelocal :
            number_of_piece_type_local(nineteen)
        with naturemutation :
            number_of_piece_nature_mutation(nineteen)
        valeurfonciere , codedep = st.columns(2)
        with valeurfonciere:
            surface_land_valeur_fonciere(nineteen)
        with codedep:
            surface_land_code_departement(nineteen)
    ##2018
    if choice == '2018' :
        perceive(eighteen)
        spaces('./presentation/prix_moyens.png')
        print_mean_bien(eighteen)
        print_mean_bien_m2(eighteen)
        print_evolution_year(nineteen,eighteen)
        print_evolution_month(eighteen)
        spaces('./presentation/diagramme_circulaire.png')
        Type_local, Nature_mutation = st.columns(2)
        with Type_local:
            chart_type_local_by_years(eighteen,2018)
        with Nature_mutation:
            chart_nature_mutation_by_years(eighteen,2018)
        spaces('./presentation/carte.png')
        mapping(eighteen,2018)

        spaces('./presentation/histo.png')
        st.write('**Valeur fonciere en fonction de la surface réeele du batiment**')
        plot_dist(eighteen,'surface_reelle_bati','#0a0403')
       
        st.write('**Valeur fonciere en fonction du nombre de piece principale**')
        plot_dist(eighteen,'nombre_pieces_principales','#0a0403')
    
        st.write('**Valeur fonciere en fonction de la surface réeele du terrain**')
        plot_dist(eighteen,'surface_terrain','#0a0403')
        spaces('./presentation/communes.png')

        number_of_cities(eighteen)
        spaces('./presentation/heatmap.png')
        Afficher = st.button('Afficher la Heatmap')
        if Afficher :
            number_main_room_real_surface(eighteen)
        spaces('./presentation/nuagedepoints.png')
        typelocal, naturemutation = st.columns(2)
        with typelocal :
            number_of_piece_type_local(eighteen)
        with naturemutation :
            number_of_piece_nature_mutation(eighteen)
        valeurfonciere , codedep = st.columns(2)
        with valeurfonciere:
            surface_land_valeur_fonciere(eighteen)
        with codedep:
            surface_land_code_departement(eighteen)
    ##2017
    if choice == '2017' :
        perceive(seventeen)
        spaces('./presentation/prix_moyens.png')
        print_mean_bien(seventeen)
        print_mean_bien_m2(seventeen)
        print_evolution_year(seventeen,seventeen)
        print_evolution_month(seventeen)
        spaces('./presentation/diagramme_circulaire.png')
        Type_local, Nature_mutation = st.columns(2)
        with Type_local:
            chart_type_local_by_years(seventeen,2017)
        with Nature_mutation:
            chart_nature_mutation_by_years(seventeen,2017)
        spaces('./presentation/carte.png')
        mapping(seventeen,2017)
        spaces('./presentation/histo.png')

        st.write('**Valeur fonciere en fonction de la surface réeele du batiment**')
        plot_dist(seventeen,'surface_reelle_bati','#0a0403')
       
        st.write('**Valeur fonciere en fonction du nombre de piece principale**')
        plot_dist(seventeen,'nombre_pieces_principales','#0a0403')
    
        st.write('**Valeur fonciere en fonction de la surface réeele du terrain**')
        plot_dist(seventeen,'surface_terrain','#0a0403')

        spaces('./presentation/communes.png')
        number_of_cities(seventeen)
        spaces('./presentation/heatmap.png')
        Afficher = st.button('Afficher la Heatmap')
        if Afficher :
            number_main_room_real_surface(seventeen)
        spaces('./presentation/nuagedepoints.png')
        typelocal, naturemutation = st.columns(2)
        with typelocal :
            number_of_piece_type_local(seventeen)
        with naturemutation :
            number_of_piece_nature_mutation(seventeen)
        valeurfonciere , codedep = st.columns(2)
        with valeurfonciere:
            surface_land_valeur_fonciere(seventeen)
        with codedep:
            surface_land_code_departement(seventeen)


if __name__ == "__main__":
    body()
