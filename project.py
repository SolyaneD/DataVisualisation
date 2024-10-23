import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import altair as alt


with st.sidebar:
    st.image("efrei.png")
    Name = st.title("Solyane DENIS")
    job = st.write("#### Data ingineer student")
    st.write("# Information de contact")
    email = st.write("**Email :** solyane.denis@efrei.net")
    linkedIn = st.write("**LinkedIn :** www.linkedin.com/in/solyane-denis")
    github = st.write("**Github :** https://github.com/SolyaneD")
    show_portfolio = st.checkbox("Voir mon portfolio")

if show_portfolio:
    st.balloons()
    st.write("### About me")
    st.write("I am a passionate and driven M1 Data Engineering student at EFREI Paris, with a strong foundation in data processing, analytics, and engineering. My academic journey has equipped me with a solid understanding of big data technologies, machine learning, and cloud platforms. I am eager to apply my knowledge in real-world applications and contribute to impactful projects. My goal is to become a proficient Data Engineer, developing innovative data solutions to solve complex business challenges.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Education")
        

    with col2:
        st.header("Skills")
        

    with col3:
        st.header("Experience")
        
    tab1, tab2, tab3 = st.tabs(["Education", "Skills", "Experience"])

    with tab1:
        st.header("Education")
        st.write("### Master 1 in Data Engineering")
        st.write("**EFREI Paris**")
        st.write("Sept 2023 – Present")
        st.write("""
        - Coursework: Big Data Frameworks, Machine Learning, Data Mining, Cloud Computing
        - Key Projects: 
            - Real-Time Data Processing Pipeline with Spark Streaming
        """)

        st.write("### Preparatory class MPSI")
        st.write('**Lycée Mariette')
        st.write('Sept 2021 - July 2023')
        st.write('Coursework : Mathematics, physics, informatic')

        st.write("### Baccalauréat")
        st.write('**Lycée Audiberti')
        st.write('July 2021')
        st.write('Coursework : Mathematics, physics, informatic')

    with tab2:
        st.header("Skills")
        
        st.write("### Programming Languages:")
        st.write("- Python, Java, SQL, C")

        st.write("### Data Engineering Tools:")
        st.write("- Apache Spark, Hadoop")

        st.write("### Databases:")
        st.write("- MySQL")

        st.write("### Machine Learning & Data Science:")
        st.write("- Scikit-learn, TensorFlow, Pandas, NumPy")

    with tab3:
        st.header("Experience")
        
        st.write("### Solution engineer intern")
        st.write("**DEEPKI**")
        st.write("November2024 - April 2025")
        st.write("""
        - Designed and implemented scalable data pipelines with Apache Spark.
        - Created ETL workflows to ingest data from various sources into cloud storage.
        """)

st.title("Description de la base de données des accidents corporels de la circulation routière - 2022")
st.write("La base de données annuelle sur les accidents corporels de la circulation routière, couvrant la période de 2005 à 2022, constitue une ressource inestimable pour comprendre et analyser les dynamiques de la sécurité routière en France. Gérée par l'Observatoire national interministériel de la sécurité routière (ONISR), cette base regroupe des informations détaillées sur chaque accident survenu sur les voies publiques, impliquant au moins un véhicule et ayant entraîné des victimes nécessitant des soins médicaux.")
st.write("Chaque incident est soigneusement documenté par les forces de l'ordre intervenant sur les lieux, permettant une collecte de données systématique et rigoureuse, qui se traduit par un ensemble de fiches intitulées \"bulletin d’analyse des accidents corporels\". Ces fiches incluent des détails sur la localisation, les caractéristiques des accidents, les types de véhicules impliqués, et les usagers affectés.")
st.write("Au fil des ans, cette base de données a évolué, offrant des enregistrements annuels depuis 2005. Elle est composée de quatre fichiers clés : Caractéristiques, Lieux, Véhicules, et Usagers, tous disponibles au format CSV pour une exploitation facile. Cependant, il est crucial de noter que certaines données relatives aux usagers et aux comportements des véhicules sont omises pour protéger la vie privée et éviter tout préjudice potentiel.")
st.subheader("Une histoire de données et de prévention")
st.write("Ces données racontent une histoire à la fois troublante et révélatrice. Elles mettent en lumière des tendances inquiétantes, comme l'augmentation de certains types d'accidents en milieu urbain ou les dangers liés à la vitesse excessive. Chaque chiffre représente une vie, une histoire, et souvent un drame familial. Par exemple, l'analyse des accidents de nuit, dans des conditions d'éclairage variables, révèle des schémas qui peuvent guider les politiques de sécurité routière, comme l'amélioration de l'éclairage public et la sensibilisation des conducteurs sur les dangers nocturnes.")
st.write("Depuis 2018, les modifications apportées aux processus de saisie des données ont rendu difficile la comparaison avec les années précédentes, illustrant ainsi les défis permanents auxquels font face les organismes de sécurité routière pour maintenir des statistiques fiables. L'ajout des usagers en fuite en 2021, bien que nécessaire, souligne également le manque d'informations sur ces cas, notamment sur la gravité des blessures.")
st.subheader("Vers une route plus sûre")
st.write("Ces données, en dépit de leurs limitations, offrent une occasion précieuse pour les décideurs, les chercheurs et le grand public de mieux comprendre les causes des accidents et de développer des stratégies efficaces de prévention. Grâce à l'engagement continu envers la collecte et l'analyse des données, nous pouvons espérer une réduction significative des accidents sur nos routes, garantissant ainsi un avenir plus sûr pour tous les usagers de la route.")
st.write("The data base : https://www.data.gouv.fr/fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2022/")


@st.cache_data
def load_data():
    caracteristiques = pd.read_csv("carcteristiques-2022.csv", delimiter=';')
    lieux = pd.read_csv("lieux-2022.csv", delimiter =';')
    usagers = pd.read_csv("usagers-2022.csv", delimiter =';')
    vehicules = pd.read_csv("vehicules-2022.csv", delimiter =';')
    return caracteristiques, lieux, usagers, vehicules

caracteristiques, lieux, usagers, vehicules = load_data()

caracteristiques['hrmn'] = pd.to_datetime(caracteristiques['hrmn'], format='%H:%M').dt.time
caracteristiques['datetime'] = pd.to_datetime(caracteristiques[['an', 'mois', 'jour']].astype(str).agg('-'.join, axis=1) + ' ' + caracteristiques['hrmn'].astype(str))
caracteristiques['hour'] = caracteristiques['datetime'].dt.hour
caracteristiques['weekday'] = caracteristiques['datetime'].dt.weekday
caracteristiques['lat'] = caracteristiques['lat'].str.replace(',', '.', regex=False)
caracteristiques['long'] = caracteristiques['long'].str.replace(',', '.', regex=False)
caracteristiques['lat'] = pd.to_numeric(caracteristiques['lat'], errors='coerce')
caracteristiques['long'] = pd.to_numeric(caracteristiques['long'], errors='coerce')
caracteristiques.rename(columns={'Accident_Id': 'Num_Acc'}, inplace=True)

merged_us_li = pd.merge(usagers, lieux, on='Num_Acc', how='inner')
merged_ca_us = pd.merge(caracteristiques, usagers, on='Num_Acc', how='inner')
merged_vh_us = pd.merge(vehicules, usagers, on='Num_Acc', how='inner')


st.header("Comprendre les données")
car, lie, vehi, usa = st.tabs(["Caractéristiques", "Lieux", "Véhicules", "Usagers"])

with car:
        if st.checkbox('Données brutes', key='carac'):
            st.write(caracteristiques)
        st.markdown("""
        **Num_Acc** : Numéro d'identifiant de l'accident.  
        **jour** : Jour de l'accident.  
        **mois** : Mois de l'accident.  
        **an** : Année de l'accident.  
        **hrmn** : Heure et minutes de l'accident.  
        **lum** : Lumière - conditions d’éclairage dans lesquelles l'accident s'est produit :  
        - 1 – Plein jour  
        - 2 – Crépuscule ou aube  
        - 3 – Nuit sans éclairage public  
        - 4 – Nuit avec éclairage public non allumé  
        - 5 – Nuit avec éclairage public allumé  

        **dep** : Département - Code INSEE du département (2A Corse-du-Sud – 2B Haute-Corse).  
        **com** : Commune - Le numéro de commune est un code donné par l’INSEE.  
        **agg** : Localisation :  
        - 1 – Hors agglomération  
        - 2 – En agglomération  

        **int** : Intersection :  
        - 1 – Hors intersection  
        - 2 – Intersection en X  
        - 3 – Intersection en T  
        - 4 – Intersection en Y  
        - 5 – Intersection à plus de 4 branches  
        - 6 – Giratoire  
        - 7 – Place  
        - 8 – Passage à niveau  
        - 9 – Autre intersection  

        **atm** : Conditions atmosphériques :  
        - -1 – Non renseigné  
        - 1 – Normale  
        - 2 – Pluie légère  
        - 3 – Pluie forte  
        - 4 – Neige - grêle  
        - 5 – Brouillard - fumée  
        - 6 – Vent fort - tempête  
        - 7 – Temps éblouissant  
        - 8 – Temps couvert  
        - 9 – Autre  

        **col** : Type de collision :  
        - -1 – Non renseigné  
        - 1 – Deux véhicules - frontale  
        - 2 – Deux véhicules – par l’arrière  
        - 3 – Deux véhicules – par le côté  
        - 4 – Trois véhicules et plus – en chaîne  
        - 5 – Trois véhicules et plus - collisions multiples  
        - 6 – Autre collision  
        - 7 – Sans collision  

        **adr** : Adresse postale - variable renseignée pour les accidents survenus en agglomération.  
        **lat** : Latitude.  
        **long** : Longitude.  
        """)

with lie:
        if st.checkbox('Données brutes', key='lieux'):
            st.write(lieux)
        st.markdown("""
        **Num_Acc** : Identifiant de l’accident identique à celui du fichier "rubrique CARACTERISTIQUES" repris dans l’accident.  
        **catr** : Catégorie de route :  
        - 1 – Autoroute  
        - 2 – Route nationale  
        - 3 – Route Départementale  
        - 4 – Voie Communale  
        - 5 – Hors réseau public  
        - 6 – Parc de stationnement ouvert à la circulation publique  
        - 7 – Routes de métropole urbaine  
        - 9 – Autre  

        **voie** : Numéro de la route.  
        **V1** : Indice numérique du numéro de route (exemple : 2 bis, 3 ter, etc.).  
        **V2** : Lettre indice alphanumérique de la route.  
        **circ** : Régime de circulation :  
        - -1 – Non renseigné  
        - 1 – A sens unique  
        - 2 – Bidirectionnelle  
        - 3 – A chaussées séparées  
        - 4 – Avec voies d’affectation variable  

        **nbv** : Nombre total de voies de circulation.  
        **vosp** : Signale l’existence d’une voie réservée :  
        - -1 – Non renseigné  
        - 0 – Sans objet  
        - 1 – Piste cyclable  
        - 2 – Bande cyclable  
        - 3 – Voie réservée  

        **prof** : Profil en long (déclivité de la route) :  
        - -1 – Non renseigné  
        - 1 – Plat  
        - 2 – Pente  
        - 3 – Sommet de côte  
        - 4 – Bas de côte  

        **pr** : Numéro du PR de rattachement (borne amont). La valeur -1 signifie non renseigné.  
        **pr1** : Distance en mètres au PR. La valeur -1 signifie non renseigné.  
        **plan** : Tracé en plan :  
        - -1 – Non renseigné  
        - 1 – Partie rectiligne  
        - 2 – En courbe à gauche  
        - 3 – En courbe à droite  
        - 4 – En « S »  

        **lartpc** : Largeur du terre-plein central (en m).  
        **larrout** : Largeur de la chaussée (en m, sans inclure bandes d’arrêt ou stationnement).  

        **surf** : État de la surface :  
        - -1 – Non renseigné  
        - 1 – Normale  
        - 2 – Mouillée  
        - 3 – Flaques  
        - 4 – Inondée  
        - 5 – Enneigée  
        - 6 – Boue  
        - 7 – Verglacée  
        - 8 – Corps gras – huile  
        - 9 – Autre  

        **infra** : Aménagement - Infrastructure :  
        - -1 – Non renseigné  
        - 0 – Aucun  
        - 1 – Souterrain - tunnel  
        - 2 – Pont - autopont  
        - 3 – Bretelle d’échangeur ou de raccordement  
        - 4 – Voie ferrée  
        - 5 – Carrefour aménagé  
        - 6 – Zone piétonne  
        - 7 – Zone de péage  
        - 8 – Chantier  
        - 9 – Autre  

        **situ** : Situation de l’accident :  
        - -1 – Non renseigné  
        - 0 – Aucun  
        - 1 – Sur chaussée  
        - 2 – Sur bande d’arrêt d’urgence  
        - 3 – Sur accotement  
        - 4 – Sur trottoir  
        - 5 – Sur piste cyclable  
        - 6 – Sur autre voie spéciale  
        - 8 – Autres  

        **vma** : Vitesse maximale autorisée sur le lieu de l’accident.
        """)

with vehi:
        if st.checkbox('Données brutes', key='vehi'):
            st.write(vehicules)
        st.markdown("""
        **Num_Acc** : Identifiant de l’accident identique à celui du fichier "rubrique CARACTERISTIQUES" repris pour chacun des véhicules décrits impliqués dans l’accident.  

        **id_vehicule** : Identifiant unique du véhicule repris pour chacun des usagers occupant ce véhicule (y compris les piétons rattachés aux véhicules qui les ont heurtés) – Code numérique.  

        **Num_Veh** : Identifiant du véhicule repris pour chacun des usagers occupant ce véhicule (y compris les piétons rattachés aux véhicules qui les ont heurtés) – Code alphanumérique.  

        **senc** : Sens de circulation :  
        - -1 – Non renseigné  
        - 0 – Inconnu  
        - 1 – PK ou PR ou numéro d’adresse postale croissant  
        - 2 – PK ou PR ou numéro d’adresse postale décroissant  
        - 3 – Absence de repère  

        **catv** : Catégorie du véhicule :  
        - 00 – Indéterminable  
        - 01 – Bicyclette  
        - 02 – Cyclomoteur <50 cm3  
        - 03 – Voiturette (Quadricycle à moteur carrossé)  
        - 04 – Référence inutilisée depuis 2006 (scooter immatriculé)  
        - 05 – Référence inutilisée depuis 2006 (motocyclette)  
        - 06 – Référence inutilisée depuis 2006 (side-car)  
        - 07 – VL seul  
        - 08 – Référence inutilisée depuis 2006 (VL + caravane)  
        - 09 – Référence inutilisée depuis 2006 (VL + remorque)  
        - 10 – VU seul 1,5T <= PTAC <= 3,5T avec ou sans remorque  
        - 11 – Référence inutilisée depuis 2006 (VU (10) + caravane)  
        - 12 – Référence inutilisée depuis 2006 (VU (10) + remorque)  
        - 13 – PL seul 3,5T <PTCA <= 7,5T  
        - 14 – PL seul > 7,5T  
        - 15 – PL > 3,5T + remorque  
        - 16 – Tracteur routier seul  
        - 17 – Tracteur routier + semi-remorque  
        - 18 – Référence inutilisée depuis 2006 (transport en commun)  
        - 19 – Référence inutilisée depuis 2006 (tramway)  
        - 20 – Engin spécial  
        - 21 – Tracteur agricole  
        - 30 – Scooter < 50 cm3  
        - 31 – Motocyclette > 50 cm3 et <= 125 cm3  
        - 32 – Scooter > 50 cm3 et <= 125 cm3  
        - 33 – Motocyclette > 125 cm3  
        - 34 – Scooter > 125 cm3  
        - 35 – Quad léger <= 50 cm3 (Quadricycle à moteur non carrossé)  
        - 36 – Quad lourd > 50 cm3 (Quadricycle à moteur non carrossé)  
        - 37 – Autobus  
        - 38 – Autocar  
        - 39 – Train  
        - 40 – Tramway  
        - 41 – 3RM <= 50 cm3  
        - 42 – 3RM > 50 cm3 <= 125 cm3  
        - 43 – 3RM > 125 cm3  
        - 50 – EDP à moteur  
        - 60 – EDP sans moteur  
        - 80 – VAE  
        - 99 – Autre véhicule  

        **obs** : Obstacle fixe heurté :  
        - -1 – Non renseigné  
        - 0 – Sans objet  
        - 1 – Véhicule en stationnement  
        - 2 – Arbre  
        - 3 – Glissière métallique  
        - 4 – Glissière béton  
        - 5 – Autre glissière  
        - 6 – Bâtiment, mur, pile de pont  
        - 7 – Support de signalisation verticale ou poste d’appel d’urgence  
        - 8 – Poteau  
        - 9 – Mobilier urbain  
        - 10 – Parapet  
        - 11 – Ilot, refuge, borne haute  
        - 12 – Bordure de trottoir  
        - 13 – Fossé, talus, paroi rocheuse  
        - 14 – Autre obstacle fixe sur chaussée  
        - 15 – Autre obstacle fixe sur trottoir ou accotement  
        - 16 – Sortie de chaussée sans obstacle  
        - 17 – Buse – tête d’aqueduc  

        **obsm** : Obstacle mobile heurté :  
        - -1 – Non renseigné  
        - 0 – Aucun  
        - 1 – Piéton  
        - 2 – Véhicule  
        - 4 – Véhicule sur rail  
        - 5 – Animal domestique  
        - 6 – Animal sauvage  
        - 9 – Autre  

        **choc** : Point de choc initial :  
        - -1 – Non renseigné  
        - 0 – Aucun  
        - 1 – Avant  
        - 2 – Avant droit  
        - 3 – Avant gauche  
        - 4 – Arrière  
        - 5 – Arrière droit  
        - 6 – Arrière gauche  
        - 7 – Côté droit  
        - 8 – Côté gauche  
        - 9 – Chocs multiples (tonneaux)  

        **manv** : Manœuvre principale avant l’accident :  
        - -1 – Non renseigné  
        - 0 – Inconnue  
        - 1 – Sans changement de direction  
        - 2 – Même sens, même file  
        - 3 – Entre 2 files  
        - 4 – En marche arrière  
        - 5 – A contresens  
        - 6 – En franchissant le terre-plein central  
        - 7 – Dans le couloir bus, dans le même sens  
        - 8 – Dans le couloir bus, dans le sens inverse  
        - 9 – En s’insérant  
        - 10 – En faisant demi-tour sur la chaussée  
        - 11 – A gauche  
        - 12 – A droite  
        - 13 – A gauche (Déporté)  
        - 14 – A droite (Déporté)  
        - 15 – A gauche (Tournant)  
        - 16 – A droite (Tournant)  
        - 17 – A gauche (Dépassant)  
        - 18 – A droite (Dépassant)  
        - 19 – Traversant la chaussée  
        - 20 – Manœuvre de stationnement  
        - 21 – Manœuvre d’évitement  
        - 22 – Ouverture de porte  
        - 23 – Arrêté (hors stationnement)  
        - 24 – En stationnement (avec occupants)  
        - 25 – Circulant sur trottoir  
        - 26 – Autres manœuvres  

        **motor** : Type de motorisation du véhicule :  
        - -1 – Non renseigné  
        - 0 – Inconnue  
        - 1 – Hydrocarbures  
        - 2 – Hybride électrique  
        - 3 – Electrique  
        - 4 – Hydrogène  
        - 5 – Humaine  
        - 6 – Autre  

        **occutc** : Nombre d’occupants dans le transport en commun.  
        """)

with usa:
        if st.checkbox('Données brutes', key='usa'):
            st.write(usagers)
        st.markdown("""
        **Num_Acc** : Identifiant de l’accident identique à celui du fichier "rubrique CARACTERISTIQUES" repris pour chacun des usagers décrits impliqués dans l’accident.  

        **id_usager** : Identifiant unique de l’usager (y compris les piétons qui sont rattachés aux véhicules qui les ont heurtés) – Code numérique.  

        **id_vehicule** : Identifiant unique du véhicule repris pour chacun des usagers occupant ce véhicule (y compris les piétons qui sont rattachés aux véhicules qui les ont heurtés) – Code numérique.  

        **num_Veh** : Identifiant du véhicule repris pour chacun des usagers occupant ce véhicule (y compris les piétons qui sont rattachés aux véhicules qui les ont heurtés) – Code alphanumérique.  

        **place** : Permet de situer la place occupée dans le véhicule par l'usager au moment de l'accident. Le détail est donné par l’illustration ci-dessous :  
        - 10 – Piéton (non applicable)  

        **catu** : Catégorie d'usager :  
        - 1 – Conducteur  
        - 2 – Passager  
        - 3 – Piéton  

        **grav** : Gravité de blessure de l'usager, les usagers accidentés sont classés en trois catégories de victimes plus les indemnes :  
        - 1 – Indemne  
        - 2 – Tué  
        - 3 – Blessé hospitalisé  
        - 4 – Blessé léger  

        **sexe** : Sexe de l'usager :  
        - 1 – Masculin  
        - 2 – Féminin  

        **An_nais** : Année de naissance de l'usager.  

        **trajet** : Motif du déplacement au moment de l’accident :  
        - -1 – Non renseigné  
        - 0 – Non renseigné  
        - 1 – Domicile – travail  
        - 2 – Domicile – école  
        - 3 – Courses – achats  
        - 4 – Utilisation professionnelle  
        - 5 – Promenade – loisirs  
        - 9 – Autre  

        Les équipements de sécurité jusqu’en 2018 étaient en 2 variables : existence et utilisation. À partir de 2019, il s’agit de l’utilisation avec jusqu’à 3 équipements possibles pour un même usager (notamment pour les motocyclistes dont le port du casque et des gants est obligatoire).  

        **secu1** : Le renseignement du caractère indique la présence et l’utilisation de l’équipement de sécurité :  
        - -1 – Non renseigné  
        - 0 – Aucun équipement  
        - 1 – Ceinture  
        - 2 – Casque  
        - 3 – Dispositif enfants  
        - 4 – Gilet réfléchissant  
        - 5 – Airbag (2RM/3RM)  
        - 6 – Gants (2RM/3RM)  
        - 7 – Gants + Airbag (2RM/3RM)  
        - 8 – Non déterminable  
        - 9 – Autre  

        **secu2** : Le renseignement du caractère indique la présence et l’utilisation de l’équipement de sécurité :  
        - -1 – Non renseigné  
        - 0 – Aucun équipement  
        - 1 – Ceinture  
        - 2 – Casque  
        - 3 – Dispositif enfants  
        - 4 – Gilet réfléchissant  
        - 5 – Airbag (2RM/3RM)  
        - 6 – Gants (2RM/3RM)  
        - 7 – Gants + Airbag (2RM/3RM)  
        - 8 – Non déterminable  
        - 9 – Autre  

        **secu3** : Le renseignement du caractère indique la présence et l’utilisation de l’équipement de sécurité :  
        - -1 – Non renseigné  
        - 0 – Aucun équipement  
        - 1 – Ceinture  
        - 2 – Casque  
        - 3 – Dispositif enfants  
        - 4 – Gilet réfléchissant  
        - 5 – Airbag (2RM/3RM)  
        - 6 – Gants (2RM/3RM)  
        - 7 – Gants + Airbag (2RM/3RM)  
        - 8 – Non déterminable  
        - 9 – Autre  

        **locp** : Localisation du piéton :  
        - -1 – Non renseigné  
        - 0 – Sans objet  
        - 1 – A + 50 m du passage piéton  
        - 2 – A – 50 m du passage piéton  
        - 3 – Sans signalisation lumineuse (sur passage piéton)  
        - 4 – Avec signalisation lumineuse (sur passage piéton)  
        - 5 – Sur trottoir  
        - 6 – Sur accotement  
        - 7 – Sur refuge ou BAU  
        - 8 – Sur contre-allée  
        - 9 – Inconnue  

        **actp** : Action du piéton :  
        - -1 – Non renseigné  
        - 0 – Non renseigné ou sans objet  
        - 1 – Sens véhicule heurtant  
        - 2 – Sens inverse du véhicule  
        - 3 – Traversant  
        - 4 – Masqué  
        - 5 – Jouant – courant  
        - 6 – Avec animal  
        - 9 – Autre  
        - A – Monte/descend du véhicule  
        - B – Inconnue  

        **etatp** : Cette variable permet de préciser si le piéton accidenté était seul ou non :  
        - -1 – Non renseigné  
        - 1 – Seul  
        - 2 – Accompagné  
        - 3 – En groupe  
        """)



tables = {
    'caracteristiques': caracteristiques,
    'lieux': lieux,
    'usagers': usagers,
    'vehicules': vehicules
}

st.header("Analysez par vous-même")
selected_table = st.selectbox("Choisissez une table", options=list(tables.keys()))

df_selected = tables[selected_table]

selected_column = st.selectbox("Choisissez une colonne à visualiser", options=df_selected.columns)

st.write(f"Vous explorez la colonne `{selected_column}` de la table `{selected_table}`")
st.write(df_selected[[selected_column]])

if pd.api.types.is_numeric_dtype(df_selected[selected_column]):
    fig, ax = plt.subplots()
    sns.histplot(df_selected[selected_column], ax=ax)
    plt.title(f"Distribution de {selected_column}")
    st.pyplot(fig)

else:
    counts = df_selected[selected_column].value_counts()
    top_counts = counts.nlargest(10)
    fig, ax = plt.subplots()
    ax.pie(top_counts, labels=top_counts.index, startangle=140)
    plt.title(f"Répartition de {selected_column}")
    st.pyplot(fig)

    

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Annalyse temporelle", "Analyse des victimes", "Analyses des conditions", "Analyse des véhicules", "Analyse des lieux"])

with tab1:
    st.header("Analyse temporelle")

    st.subheader("Accidents par heure de la journée")
    st.bar_chart(caracteristiques['hour'].value_counts().sort_index())

    st.subheader("Accidents par mois de l'année")
    st.bar_chart(caracteristiques['mois'].value_counts().sort_index())

    st.subheader("Accident par jour du mois")
    st.bar_chart(caracteristiques['jour'].value_counts().sort_index())

    st.subheader('Accident par jour de la semaine')
    days_of_week = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']
    weekday_accidents = caracteristiques['weekday'].value_counts().reindex(np.arange(7), fill_value=0)
    weekday_accidents.index = pd.CategoricalIndex(days_of_week, categories=days_of_week, ordered=True)
    st.bar_chart(weekday_accidents)

with tab2:
    st.header("Analyse des victimes")

    victim_count = usagers['catu'].value_counts().reset_index()
    victim_count.columns = ['Type de victime', 'Nombre de victimes']
    chart = alt.Chart(victim_count).mark_bar().encode(
        x=alt.X('Type de victime:O', title='Type de Victime'),
        y=alt.Y('Nombre de victimes:Q', title='Nombre de Victimes'),
        color=alt.Color('Type de victime:O', scale=alt.Scale(scheme='viridis'))
    ).properties(
        title='Distribution des types de victimes'
    )
    st.altair_chart(chart, use_container_width=True)

    with st.expander("Voir explication"):
     st.write("""
    Catégorie d'usager :  
    1 – Conducteur   
    2 – Passager   
    3 – Piéton  
     """)

    current_year = 2024
    usagers['age'] = current_year - usagers['an_nais']
    age_distribution = usagers.groupby(['age', 'grav']).size().reset_index(name='Nombre de Victimes')
    chart = alt.Chart(age_distribution).mark_bar().encode(
        x=alt.X('age:O', title='Âge'),
        y=alt.Y('Nombre de Victimes:Q', title='Nombre de Victimes'),
        color=alt.Color('grav:O', 
                        scale=alt.Scale(scheme='category10'),
                        title='Type de Victime'),
        tooltip=[alt.Tooltip('age:O', title='Âge'), 
                 alt.Tooltip('Nombre de Victimes:Q', title='Nombre de Victimes'),
                 alt.Tooltip('grav:O', title='Type de Victime')]
    ).properties(
        width=600,
        height=400,
        title='Pyramide des âges des victimes par gravité'
    )
    st.subheader('Pyramide des âges des victimes par gravité')
    st.altair_chart(chart, use_container_width=True)

    with st.expander("Voir explication"):
     st.write("""
    Gravité de blessure de l'usager, les usagers accidentés sont classés en trois catégories de 
    victimes plus les indemnes :  
    1 – Indemne   
    2 – Tué   
    3 – Blessé hospitalisé   
    4 – Blessé léger 
     """)


    current_year = 2024
    usagers['age'] = current_year - usagers['an_nais']
    age_distribution = usagers.groupby(['age', 'catu']).size().reset_index(name='Nombre de Victimes')
    chart = alt.Chart(age_distribution).mark_bar().encode(
        x=alt.X('age:O', title='Âge'),
        y=alt.Y('Nombre de Victimes:Q', title='Nombre de Victimes'),
        color=alt.Color('catu:O', 
                        scale=alt.Scale(scheme='category10'),
                        title='Type de Victime'),
        tooltip=[alt.Tooltip('catu:O', title='Âge'), 
                 alt.Tooltip('Nombre de Victimes:Q', title='Nombre de Victimes'),
                 alt.Tooltip('catu:O', title='Type de Victime')]
    ).properties(
        width=600,
        height=400,
        title='Pyramide des âges des victimes par type'
    )
    st.subheader('Pyramide des âges des victimes par type')
    st.altair_chart(chart, use_container_width=True)

    with st.expander("Voir explication"):
     st.write("""
    Catégorie d'usager :  
    1 – Conducteur   
    2 – Passager   
    3 – Piéton  
     """)


    sex_distribution = usagers['sexe'].value_counts()
    colors = ['orange', 'purple', 'red']

    fig1, ax1 = plt.subplots()
    ax1.pie(sex_distribution, labels=sex_distribution.index, autopct='%1.1f%%', startangle=90, colors=colors)
    ax1.axis('equal')
    plt.title('Répartition des Victimes par Sexe')
    fig2, ax2 = plt.subplots()
    usagers['sexe'].value_counts().sort_index().plot(kind='bar', ax=ax2, color=colors)
    ax2.set_title('Répartition des victimes par sexe (barres)')
    ax2.set_xlabel('Sexe')
    ax2.set_ylabel('Nombre de Victimes')
    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Répartition des victimes par sexe (camembert)')
        st.pyplot(fig1)

    with col2:
        st.subheader('Répartition des victimes par sexe (barres)')
        st.pyplot(fig2)

    with st.expander("Voir explication"):
        st.write("""
        Sexe de l'usager :  
        1 – Masculin   
        2 – Féminin

        -1 –  Non renseigné
        """)

with tab3:
    st.header("Analyse des conditions")
    st.subheader('Nombre d\'accidents par conditions atmosphériques')
    atm_counts = caracteristiques['atm'].value_counts()
    st.bar_chart(atm_counts)
    with st.expander("Voir explication"):
     st.write("""
         Conditions atmosphériques :
         -1 – Non renseigné  
         1 – Normale  
         2 – Pluie légère  
         3 – Pluie forte  
         4 – Neige - grêle  
         5 – Brouillard - fumée  
         6 – Vent fort - tempête  
         7 – Temps éblouissant  
         8 – Temps couvert  
         9 – Autre 
     """)


    st.subheader('Nombre d\'accidents par conditions d\'éclairage')
    lum_counts = caracteristiques['lum'].value_counts()
    st.bar_chart(lum_counts)
    lum_counts.plot(kind='bar', color='salmon')
    with st.expander("Voir explication"):
     st.write("""
    Lumière : conditions d’éclairage dans lesquelles l'accident s'est produit :  
    1 – Plein jour  
    2 – Crépuscule ou aube  
    3 – Nuit sans éclairage public  
    4 – Nuit avec éclairage public non allumé  
    5 – Nuit avec éclairage public allumé  
     """)


    st.subheader("Nombre d'accidents par conditions d'éclairage et atmosphériques")
    pivot_table = pd.crosstab(caracteristiques['lum'], caracteristiques['atm'], 
                           rownames=['Conditions d\'éclairage'], 
                           colnames=['Conditions Atmosphériques'], 
                           margins=False)
    chart_data = pivot_table.T
    st.bar_chart(chart_data)
    with st.expander("Voir les explications"):
        st.write("""
    Conditions d'éclairage :
    1 – Plein jour 
    2 – Crépuscule ou aube  
    3 – Nuit sans éclairage public  
    4 – Nuit avec éclairage public non allumé  
    5 – Nuit avec éclairage public allumé  
    
    Conditions atmosphériques :
    1 – Normale  
    2 – Pluie légère  
    3 – Pluie forte  
    4 – Neige - grêle  
    5 – Brouillard - fumée  
    6 – Vent fort - tempête  
    7 – Temps éblouissant  
    8 – Temps couvert  
    9 – Autre  
    """)


    st.subheader("Analyse de la vitesse maximale autorisée par gravité de l'accident")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='grav', y='vma', data=merged_us_li, palette='Set2', ax=ax)
    ax.set_title('Vitesse Maximale Autorisée par Gravité de l\'Accident')
    ax.set_xlabel('Gravité de l\'Accident')
    ax.set_ylabel('Vitesse Maximale Autorisée (km/h)')
    ax.grid(axis='y')
    st.pyplot(fig)
    correlation = merged_us_li['vma'].corr(merged_us_li['grav'])
    st.write(f'**Corrélation entre vitesse maximale autorisée et gravité de l\'accident : {correlation:.2f}**')
    with st.expander("Voir les explications"):
        st.write("""
        - **Gravité de l'accident :**
          - 1 : Indemne
          - 2 : Tué
          - 3 : Blessé hospitalisé
          - 4 : Blessé léger
        - **Vitesse Maximale Autorisée (VMA)** : Vitesse réglementaire en km/h.
        """)


    st.subheader('Nombre d\'accidents par type d\'intersection et gravité')
    intersection_counts = merged_ca_us.groupby(['int', 'grav']).size().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(10, 6))
    intersection_counts.plot(kind='bar', stacked=True, ax=ax, color=plt.cm.tab10.colors)
    ax.set_title('Nombre d\'Accidents par Type d\'Intersection et Gravité')
    ax.set_xlabel('Type d\'Intersection')
    ax.set_ylabel('Nombre d\'Accidents')
    ax.set_xticks(range(len(intersection_counts.index)))
    ax.set_xticklabels(intersection_counts.index, rotation=45)
    ax.legend(title='Gravité de l\'Accident', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(axis='y')
    plt.tight_layout()
    st.pyplot(fig)
    with st.expander("Voir les explications"):
        st.write("""
        **int** : Intersection :  
        - 1 – Hors intersection  
        - 2 – Intersection en X  
        - 3 – Intersection en T  
        - 4 – Intersection en Y  
        - 5 – Intersection à plus de 4 branches  
        - 6 – Giratoire  
        - 7 – Place  
        - 8 – Passage à niveau  
        - 9 – Autre intersection  
        - **Gravité de l'accident :**
          - 1 : Indemne
          - 2 : Tué
          - 3 : Blessé hospitalisé
          - 4 : Blessé léger
        """)

with tab4:
    st.header("Analyse des véhicules")
    vehicules_counts = vehicules['catv'].value_counts()
    top_counts = vehicules_counts.nlargest(10)
    plt.figure(figsize=(8, 8))
    top_counts.plot(kind='pie', startangle=90, colors=['skyblue', 'salmon', 'lightgreen', 'orange', 'lightcoral', 'gold', 'lightblue', 'lavender', 'lightgreen', 'lightsalmon'])
    plt.title('Proportion des 10 types de véhicules impliqués dans les accidents')
    plt.ylabel('')
    st.pyplot(plt)
    with st.expander("Voir explication"):
     st.write("""
    **catv** : Catégorie du véhicule :  
    - 00 – Indéterminable  
    - 01 – Bicyclette  
    - 02 – Cyclomoteur <50 cm3  
    - 03 – Voiturette (Quadricycle à moteur carrossé)  
    - 04 – Référence inutilisée depuis 2006 (scooter immatriculé)  
    - 05 – Référence inutilisée depuis 2006 (motocyclette)  
    - 06 – Référence inutilisée depuis 2006 (side-car)  
    - 07 – VL seul  
    - 08 – Référence inutilisée depuis 2006 (VL + caravane)  
    - 09 – Référence inutilisée depuis 2006 (VL + remorque)  
    - 10 – VU seul 1,5T <= PTAC <= 3,5T avec ou sans remorque  
    - 11 – Référence inutilisée depuis 2006 (VU (10) + caravane)  
    - 12 – Référence inutilisée depuis 2006 (VU (10) + remorque)  
    - 13 – PL seul 3,5T <PTCA <= 7,5T  
    - 14 – PL seul > 7,5T  
    - 15 – PL > 3,5T + remorque  
    - 16 – Tracteur routier seul  
    - 17 – Tracteur routier + semi-remorque  
    - 18 – Référence inutilisée depuis 2006 (transport en commun)  
    - 19 – Référence inutilisée depuis 2006 (tramway)  
    - 20 – Engin spécial  
    - 21 – Tracteur agricole  
    - 30 – Scooter < 50 cm3  
    - 31 – Motocyclette > 50 cm3 et <= 125 cm3  
    - 32 – Scooter > 50 cm3 et <= 125 cm3  
    - 33 – Motocyclette > 125 cm3  
    - 34 – Scooter > 125 cm3  
    - 35 – Quad léger <= 50 cm3 (Quadricycle à moteur non carrossé)  
    - 36 – Quad lourd > 50 cm3 (Quadricycle à moteur non carrossé)  
    - 37 – Autobus  
    - 38 – Autocar  
    - 39 – Train  
    - 40 – Tramway  
    - 41 – 3RM <= 50 cm3  
    - 42 – 3RM > 50 cm3 <= 125 cm3  
    - 43 – 3RM > 125 cm3  
    - 50 – EDP à moteur  
    - 60 – EDP sans moteur  
    - 80 – VAE  
    - 99 – Autre véhicule
     """)


    grav_by_vehicle = merged_vh_us.groupby(['catv', 'grav']).size().unstack(fill_value=0)
    plt.figure(figsize=(10, 6))
    grav_by_vehicle.plot(kind='bar', stacked=True, ax=plt.gca(), color=['green', 'yellow', 'orange', 'red'])
    plt.title('Gravité des Accidents par Type de Véhicule')
    plt.xlabel('Type de Véhicule')
    plt.ylabel('Nombre d\'Accidents')
    plt.legend(title='Gravité', labels=['Indemne', 'Blessé léger', 'Blessé grave', 'Tué'])
    plt.grid(axis='y')
    st.pyplot(plt)
    with st.expander("Voir explication"):
     st.write("""
    **grav** : Gravité de blessure de l'usager, les usagers accidentés sont classés en trois catégories de victimes plus les indemnes :  
    - 1 – Indemne  
    - 2 – Tué  
    - 3 – Blessé hospitalisé  
    - 4 – Blessé léger  
    **catv** : Catégorie du véhicule :  
    - 00 – Indéterminable  
    - 01 – Bicyclette  
    - 02 – Cyclomoteur <50 cm3  
    - 03 – Voiturette (Quadricycle à moteur carrossé)  
    - 04 – Référence inutilisée depuis 2006 (scooter immatriculé)  
    - 05 – Référence inutilisée depuis 2006 (motocyclette)  
    - 06 – Référence inutilisée depuis 2006 (side-car)  
    - 07 – VL seul  
    - 08 – Référence inutilisée depuis 2006 (VL + caravane)  
    - 09 – Référence inutilisée depuis 2006 (VL + remorque)  
    - 10 – VU seul 1,5T <= PTAC <= 3,5T avec ou sans remorque  
    - 11 – Référence inutilisée depuis 2006 (VU (10) + caravane)  
    - 12 – Référence inutilisée depuis 2006 (VU (10) + remorque)  
    - 13 – PL seul 3,5T <PTCA <= 7,5T  
    - 14 – PL seul > 7,5T  
    - 15 – PL > 3,5T + remorque  
    - 16 – Tracteur routier seul  
    - 17 – Tracteur routier + semi-remorque  
    - 18 – Référence inutilisée depuis 2006 (transport en commun)  
    - 19 – Référence inutilisée depuis 2006 (tramway)  
    - 20 – Engin spécial  
    - 21 – Tracteur agricole  
    - 30 – Scooter < 50 cm3  
    - 31 – Motocyclette > 50 cm3 et <= 125 cm3  
    - 32 – Scooter > 50 cm3 et <= 125 cm3  
    - 33 – Motocyclette > 125 cm3  
    - 34 – Scooter > 125 cm3  
    - 35 – Quad léger <= 50 cm3 (Quadricycle à moteur non carrossé)  
    - 36 – Quad lourd > 50 cm3 (Quadricycle à moteur non carrossé)  
    - 37 – Autobus  
    - 38 – Autocar  
    - 39 – Train  
    - 40 – Tramway  
    - 41 – 3RM <= 50 cm3  
    - 42 – 3RM > 50 cm3 <= 125 cm3  
    - 43 – 3RM > 125 cm3  
    - 50 – EDP à moteur  
    - 60 – EDP sans moteur  
    - 80 – VAE  
    - 99 – Autre véhicule
     """)


    vehicules_par_accident = vehicules.groupby('Num_Acc').size()
    plt.figure(figsize=(8, 6))
    vehicules_par_accident.value_counts().sort_index().plot(kind='bar', color='skyblue')
    plt.title('Nombre de Véhicules Impliqués par Accident')
    plt.xlabel('Nombre de Véhicules')
    plt.ylabel('Nombre d\'Accidents')
    plt.grid(axis='y')
    st.pyplot(plt)


    vehicules_par_accident = vehicules.groupby('Num_Acc').size().reset_index(name='nb_vehicules')
    accidents_gravite_vehicules = pd.merge(vehicules_par_accident, usagers[['Num_Acc', 'grav']], on='Num_Acc')
    gravite_vehicules_count = accidents_gravite_vehicules.groupby(['nb_vehicules', 'grav']).size().unstack(fill_value=0)
    plt.figure(figsize=(10, 6))
    gravite_vehicules_count.plot(kind='bar', stacked=True, color=['green', 'yellow', 'orange', 'red'], ax=plt.gca())
    plt.title('Gravité des Victimes en Fonction du Nombre de Véhicules Impliqués')
    plt.xlabel('Nombre de Véhicules Impliqués')
    plt.ylabel('Nombre de Victimes')
    plt.legend(title='Gravité', labels=['Indemne', 'Blessé léger', 'Blessé grave', 'Tué'])
    plt.grid(axis='y')
    st.pyplot(plt)
    with st.expander("Voir explication"):
     st.write("""
    **grav** : Gravité de blessure de l'usager, les usagers accidentés sont classés en trois catégories de victimes plus les indemnes :  
    - 1 – Indemne  
    - 2 – Tué  
    - 3 – Blessé hospitalisé  
    - 4 – Blessé léger  
     """)

with tab5:
    st.header("Analyse des lieux")
    st.subheader("Latitude et Longitude")

    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots()
        ax.hist(caracteristiques['lat'], bins=100, range=(-23.373, 51.072044), color='r', alpha=0.5)
        ax.set_xlabel('Latitude')
        ax.set_ylabel('Fréquence')
        ax.set_title('Latitude')
        st.pyplot(fig)
    with col2:
        fig, ax = plt.subplots()
        ax.hist(caracteristiques['long'], bins=100, range=(-176.201857, 168.033384), color='g', alpha=0.5)
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Fréquence')
        ax.set_title('Longitude')
        st.pyplot(fig)

    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots()
        plt.title('Longitude and Latitude', fontsize=15)
        plt.hist(caracteristiques['long'], bins = 100, range=(-176.201857, 168.033384), color = 'g', alpha = 0.5, label = 'Longitude')
        plt.legend(loc = 'best')
        plt.twiny()
        plt.hist(caracteristiques['lat'], bins = 100, range=(-23.373, 51.072044), color = 'r', alpha = 0.5, label = 'Latitude')
        plt.legend(loc = 'upper left')
        st.pyplot(fig)
    with col2:
        fig, ax = plt.subplots()
        plt.title('Longitude and Latitude', fontsize=15)
        plt.hist(caracteristiques['long'], bins = 100, range=(-10, 30), color = 'g', alpha = 0.5, label = 'Longitude')
        plt.legend(loc = 'best')
        plt.twiny()
        plt.hist(caracteristiques['lat'], bins = 100, range=(-100, 170), color = 'r', alpha = 0.5, label = 'Latitude')
        plt.legend(loc = 'upper left')
        st.pyplot(fig)

    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots()
        plt.title('Accident par longitude et latitude')
        plt.xlabel('Latitude')
        plt.ylabel('Longitude')
        plt.scatter(caracteristiques['long'], caracteristiques['lat'], color='r', s=0.8, alpha=0.4)
        plt.xlim(-176.201857, 168.033384)
        plt.ylim(-23.373, 51.072044)
        st.pyplot(fig)
    with col2:
        fig, ax = plt.subplots()
        plt.title('Accident par longitude et latitude')
        plt.xlabel('Latitude')
        plt.ylabel('Longitude')
        plt.scatter(caracteristiques['long'], caracteristiques['lat'], color='r', s=0.8, alpha=0.4)
        plt.xlim(-5, 10)
        plt.ylim(41, 51.072044)
        st.pyplot(fig)


    accidents_par_type = lieux.groupby('catr')['Num_Acc'].sum()
    fig, ax = plt.subplots()
    plt.pie(accidents_par_type, labels=accidents_par_type.index, startangle=140, colors=['lightblue', 'lightgreen', 'salmon', 'gold'])
    plt.title('Taux d\'accidents par type de route')
    plt.axis('equal')
    with st.expander("Voir explication"):
     st.write("""
        **catr** : Catégorie de route :  
        - 1 – Autoroute  
        - 2 – Route nationale  
        - 3 – Route Départementale  
        - 4 – Voie Communale  
        - 5 – Hors réseau public  
        - 6 – Parc de stationnement ouvert à la circulation publique  
        - 7 – Routes de métropole urbaine  
        - 9 – Autre  
     """)


    st.subheader("Carte des accidents")
    map_center = [caracteristiques['lat'].mean(), caracteristiques['long'].mean()]
    folium_map = folium.Map(location=map_center, zoom_start=6)
    for index, row in caracteristiques.iterrows():
        folium.CircleMarker(
            location=(row['lat'], row['long']),
            radius=5,
            color='red',
            fill=True,
            fill_color='red',
            fill_opacity=0.6,
            popup=f"Accident {index + 1}"
        ).add_to(folium_map)
    st_data = st_folium(folium_map, width=700, height=500)
