# Analyse Statistique de la Volatilité du Bitcoin

## Auteurs
Yanis Ponthou & Lucas Desperrois

## Description
Ce programme analyse la volatilité du Bitcoin en utilisant les données historiques de prix de clôture. Il calcule les statistiques de volatilité et trace des graphiques pour visualiser les résultats.

## Fonctionnalités
- Lecture des données historiques de prix de clôture à partir de fichiers CSV.
- Calcul des rendements quotidiens et de la volatilité sur 30 jours.
- Ajout de moyennes mobiles exponentielles pour la prévision des prix.
- Identification des périodes de forte volatilité.
- Tracé de graphiques pour visualiser les prix de clôture, les moyennes mobiles et la volatilité.

## Dépendances
Le programme nécessite les librairies suivantes :
- `glob`
- `matplotlib`
- `numpy`
- `pandas`
- `os`

Vous pouvez installer les dépendances en utilisant pip :
```bash
pip install matplotlib numpy pandas
```

## Utilisation

1. Placez vos fichiers CSV contenant les données historiques de prix de clôture dans le dossier `dataCrypto`.
2. Assurez-vous que les fichiers CSV ont une colonne `Date` et une colonne `Close`.
3. Exécutez le programme en lançant le fichier `indexStat.py` :
```bash
python indexStat.py
```


## Exemple de Résultat
Le programme génère des graphiques montrant l'évolution du prix de clôture avec les moyennes mobiles exponentielles et la volatilité avec indication des périodes de forte volatilité.

## Remarques
- Assurez-vous que les fichiers CSV sont correctement formatés avec les colonnes nécessaires.
- Les graphiques sont affichés à l'écran et ne sont pas enregistrés automatiquement. Vous pouvez les enregistrer manuellement si nécessaire.