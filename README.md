# Data Vizualisation


![DESCRIPTION DE L'IMAGE](https://miro.medium.com/max/724/1*u9U3YjxT9c9A1FIaDMonHw.png)
# Liens vers application créée : 
```
https://share.streamlit.io/emilefrd/dataviz/main/main.py
```
# Ressources génerales :
### Données publiques utilisées :
```
https://www.data.gouv.fr/en/datasets/demandes-de-valeurs-foncieres/
```
# Instructions et consignes
- Create a dashbord with some constraints :
-   2 internal streamlit plots : 
	- st.line / st.bar_chart / st.map
-   4 external plots 
	- Histograms, Bar, Scatter or Pie charts
-   2 checkbox
-   A slider 
-   Cache usage
-   A decorator

# Pré requis
#### In your command line, at the source of your project : 
```
streamlit run main.py
```


# Etapes de construction :
### Nétoyage de données
##### J'ai procédé de la maniere suivante : 
- Charger les données des CSV full pour les différentes années (2017 à 2020)
- Cleaner 
	- Supprimer les colonnes dans lesquelles il y a tres peu de valeurs (connues grace à pandas_profiling)
	- Supprimer les NA
	- Conserver uniquement les valeurs comprises entre le Q1 et le Q3
	- Prendre un échentillon de ce clean
- Enregistrer ce csv clean dans mon dossier CSVclean

REMARQUE : Ce nettoyage de données a été effectué dans le fichier : cleaner.py

### Réalisation de l'application 
##### Contenue dans le fichier : main.py


## Author

* **FARAMOND Emile** _alias_ [@emilefrd](https://github.com/emilefrd)
