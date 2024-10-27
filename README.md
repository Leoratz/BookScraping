# 📚 Bibliopolis - Système de Surveillance des Prix des Livres d'Occasion

Ce projet propose un système fictif de surveillance des prix pour le site d'entraînement OldBooks Finder, réalisé dans le cadre d'un exercice de scraping pour la boutique imaginaire Bibliopolis, spécialisée dans la vente de livres rares et d'occasion.

## 📋 Description du projet
<p>
Ce système permet d’extraire, d’analyser et de présenter les prix des livres de diverses catégories sur le site OldBooks Finder. Les données extraites incluent les informations de chaque livre telles que le titre, le prix, la disponibilité, la catégorie, et bien plus. En finalité, un rapport en PDF est généré, comportant des graphiques pour une analyse visuelle des prix par catégorie.
</p>
<hr>

## 🧩 Structure du projet

* ### Phase 1 : Extraction des informations d’un produit unique
* ### Phase 2 : Extraction des informations de tous les produits dans une catégorie donnée
* ### Phase 3 : Téléchargement et enregistrement des images des livres
* ### Phase 4 : Extraction des informations de toutes les catégories disponibles
* ### Phase 5 : Visualisation des données extraites avec <strong> ReportLab </strong>
* ### Phase 6 : Génération d'un rapport PDF avec <strong> ReportLab </strong>

<hr>

## 🛠️ Installation
Prérequis
<p>
Assurez-vous d’avoir Python 3.x et Git installés sur votre système.
</p>

### Cloner le dépôt :

````bash
git clone https://github.com/Leoratz/BookScraping.git
cd BookScraping
````

### Installer les dépendances :

Dans le dossier racine du projet, exécutez :
````bash
    pip install -r requirements.txt
````
### Configuration

<p>Les données collectées seront exportées dans un fichier CSV par catégorie de livres, et les images seront enregistrées dans un dossier dédié.</p>
<p>Note : Assurez-vous de ne pas inclure de fichiers CSV ou de dossiers d’images dans le dépôt Git.</p>

<hr>

## 🚀 Utilisation

<p>Les étapes 1 à 4 sont éxecutées en même temps. La visualisation des données se fait séparement.</p>
1. <strong>Phase 1-4 :</strong> Extraire les informations de toutes les catégories de livres et les stocker.

````bash
python .\app.py
````
2. <strong>Phase 5-6 :</strong> Générer un rapport PDF final avec les graphiques et les informations principales.

````bash
python .\charts.py
````
<hr>

### 📊 Visualisations

<p>Les graphiques suivants sont générés avec <strong>ReportLab</strong> et intégrés au PDF final :</p>

* 1. <strong>Diagramme circulaire :</strong> Répartition des livres par catégorie.
* 2. <strong>Graphique en barres :</strong> Prix moyen des livres par catégorie.

<hr>

### 📝 Rapport PDF
<p>Le rapport PDF (rapport_prix_livres.pdf) contient :</p>

* <strong>Titre</strong> : "Rapport des prix des livres d'occasion"
* <strong>Graphiques</strong> : Diagramme circulaire et graphique en barres
* <strong>Statistiques clés</strong> :
* Prix moyen global des livres
* Catégorie la plus représentée
* Catégorie avec le prix moyen le plus élevé
* <strong>Description</strong> : Brèves explications accompagnant chaque graphique

<hr>

### 📂 Organisation du code

* ````requirements.txt```` : Fichier listant les dépendances du projet
* ````app.py```` : Script pour extraire les données de chaques livres de toutes les catégories
* ````charts.py```` : Script pour générer les graphiques et le rapport PDF avec ReportLab

<hr>

### 📧 Contact

<p>Si vous avez des questions, n’hésitez pas à me contacter via leora@chriqui.name.</p>

<hr>
