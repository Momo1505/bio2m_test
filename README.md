# bio2m_test

## Installation

### 1. Cloner le projet
```bash
git clone git@github.com:Momo1505/bio2m_test.git
cd bio2m_test
```
### 2. Créer un environnement Python
```bash
python -m venv venv
source venv/bin/activate
```
### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```
### 4. Se connecter à Hugging Face 
```bash
huggingface-cli login
```

### 5. Préparer vos documents
Mettez vos fichiers dans le fichier ``docs``, Le script créera automatiquement une base vectorielle persistante dans ``db``

### 6. Utilisation
Lancer
```bash
python chat.py
```
### 7. Exemples
Exemple 1 

```bash
 Question: Comment sont classifiées les AHAI ?
 Recherche en cours...
 Réponse:  Les anémies hémolytiques auto-immunes (AHAI) sont classifiées en fonction des propriétés immunochimiques de l'auto-anticorps en cause. On distingue principalement les AHAI à auto-anticorps « chauds » et les AHAI à agglutinines froides (AF).

 Sources trouvées (3 documents):
 -II. Synthèse à l’intention des médecins spécialistes...
 - 2. 18 
Tableau 3 
 
Classification et caractéristiques principales des AHAI. ...
 -Au cours de l’AHAI à Ac. chauds ou froids, le recours transitoire (hors AMM) à un 
ASE peut s’avérer utile en cas de réticulocytose inadaptée...
```

Exemple 2 

```bash
 Question: Qui a coordonné le PNDS  ?
 Recherche en cours...
 Réponse:  Le PNDS a été coordonné par le Pr Marc Michel.

 Sources trouvées (3 documents):
 -Française de Sécurité Sanitaire des Produits de Santé (Afssaps) ;  des d ocuments des sites Internet  Orphanet et de la Société Française 
d’Hématologie....
 - détail les méc anismes physiopathologiques en cause dans l’AHAI  qui sont 
au-delà des objectifs pratiques du PNDS...
 -L’objectif de ce Pr otocole National de Diagnostic et de Soins (PNDS) est...
```

Exemple 3 

```bash
  Question: c'est quoi le frottis sanguin?
 Recherche en cours...
 Réponse:  Un frottis sanguin est un échantillon pris sur quelques gouttes de sang pour étudier son aspect morphologique sous le microscope..

 Sources trouvées (3 documents):
 - En cas d’hémolyse intra-vasculaire prédominante, elle peut se révèler par un 
« syndrome anémique  »...
 -De l’absence d’arguments sur  le frottis sanguin  pour une autre cause 
d’hémolyse constitutionnelle ou acquise...
 - d’hémolyse constitutionnelle  (anomalies de membrane, 
hémoglobinopathies, déficits enzymatiques)...
```
### 8. Quitter
Quittez avec ``quit`` ou ``ctrl C``
