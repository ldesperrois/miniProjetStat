# Analyse Statistique de la Volatilité des Cryptomonnaies

## Auteurs
Yanis Ponthou & Lucas Desperrois

## Description
Ce programme analyse la volatilité des cryptomonnaies en utilisant les données historiques de prix de clôture. Il calcule les statistiques de volatilité, identifie les périodes de forte volatilité, et trace des graphiques pour visualiser les résultats. Une stratégie d'achat/vente basée sur la volatilité est également implémentée pour estimer les gains potentiels avec une enveloppe donné

## Fonctionnalités
- Lecture des données historiques de prix de clôture à partir de fichiers CSV.
- Calcul des rendements quotidiens et de la volatilité sur 30 jours.
- Ajout de moyennes mobiles exponentielles (EMA) pour la prévision des prix.
- Identification des périodes de forte volatilité (basées sur un seuil dynamique : moyenne + écart-type).
- Tracé de graphiques pour visualiser :
  - Les prix de clôture avec les moyennes mobiles exponentielles.
  - La volatilité avec indication des périodes de forte volatilité.
- Implémentation d'une stratégie d'achat/vente basée sur la volatilité pour estimer les gains potentiels.

## Dépendances
Le programme nécessite les librairies suivantes :
- `glob`
- `matplotlib`
- `numpy`
- `pandas`
- `os`

### Installation des dépendances
Vous pouvez installer automatiquement les dépendances en exécutant le script 
```bash
pip install -r requirements.txt
```
ou
```bash
pip3 install -r requirements.txt

```

## Utilisation

1. **Préparation des données** :
   - Placez vos fichiers CSV contenant les données historiques de prix de clôture dans le dossier `dataCrypto`.
   - Assurez-vous que les fichiers CSV contiennent au minimum les colonnes suivantes :
     - `Date` : Date des données (format `YYYY-MM-DD` recommandé).
     - `Close` : Prix de clôture.

2. **Exécution du programme** :
   - Lancez le fichier `indexStat.py` :
     ```bash
     python indexStat.py
     ```
     ou
        ```bash
     python3 indexStat.py
     ```
3. **Résultats** :
   - Les graphiques sont générés pour chaque cryptomonnaie analysée :
     - Évolution des prix de clôture avec les moyennes mobiles exponentielles.
     - Volatilité avec indication des périodes de forte volatilité.
   - Les gains potentiels sont affichés dans la console pour chaque cryptomonnaie.


### Graphiques :
1. **Prix de clôture avec moyennes mobiles exponentielles** :
   - Ligne bleue : Prix de clôture.
   - Ligne verte : EMA 10 jours.
   - Ligne rouge : EMA 30 jours.

2. **Volatilité avec périodes de forte volatilité** :
   - Ligne rouge : Volatilité sur 30 jours.
   - Ligne noire pointillée : Seuil de forte volatilité.
   - Zones rouges : Périodes de forte volatilité.


## Structure des fichiers
- **`indexStat.py`** : Script principal contenant les calculs et la logique d'analyse.
- **`install_dependencies.py`** : Script pour installer automatiquement les dépendances.
- **`dataCrypto/`** : Dossier contenant les fichiers CSV des données historiques.
- **`resultats/`** : Dossier où les graphiques générés sont enregistrés.

## Vocabulaire

### **Volatilité**
- **Définition** : La volatilité mesure la variation des rendements d'un actif financier sur une période donnée. Elle est souvent utilisée pour évaluer le risque associé à un actif.
- **Volatilité sur 30 jours** : Calculée comme l'écart-type des rendements quotidiens sur une fenêtre glissante de 30 jours.
- **Utilité dans le projet** :
  - La volatilité est utilisée pour identifier les périodes de forte volatilité (où les variations de prix sont importantes).
  - Ces périodes influencent la stratégie d'achat/vente et sont mises en évidence sur les graphiques.

### **Moyenne Mobile Exponentielle (EMA)**
- **Définition** : L'EMA (Exponential Moving Average) est une moyenne mobile qui attribue plus de poids aux données récentes, ce qui la rend plus réactive aux variations récentes des prix.
- **EMA 10 jours** : Moyenne mobile exponentielle calculée sur une période de 10 jours. Elle est utilisée pour suivre les tendances à court terme.
- **EMA 30 jours** : Moyenne mobile exponentielle calculée sur une période de 30 jours. Elle est utilisée pour suivre les tendances à moyen terme.
- **Utilité dans le projet** :
  - Les EMA permettent de lisser les fluctuations des prix et d'identifier les tendances générales.
  - Elles sont tracées sur les graphiques pour visualiser les tendances à court et moyen terme dans notre cas.


## Remarques
- Les graphiques sont automatiquement enregistrés dans un dossier de résultats.
- Assurez-vous que les fichiers CSV sont correctement formatés avec les colonnes nécessaires.
- Vous pouvez ajuster les paramètres de la stratégie (par exemple, seuil de volatilité ou enveloppe initiale) directement dans le fichier `indexStat.py`.

