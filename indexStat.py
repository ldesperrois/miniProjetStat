"""
Author:Yanis Ponthou & Lucas Desperrois
Programme qui s'occupe de l'analyse statistique de la volatilité du Bitcoin
en utilisant les données historiques de prix de clôture.
"""


"""
Importation des librairies nécessaires
"""
import glob
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os


cheminResultat = "graphiques/"

"""
Fonction qui s'occupe d'ouvrir un csv et de le lire
"""
def openCSV():
    dfCoin = pd.read_csv("dataCrypto/Bitcoin.csv");
    return dfCoin;

"""
Fonction qui s'occupe de calculer les statistiques de volatilité
"""
def statsVolatilite(dfCoin):
    # Convertir la colonne Date en format datetime
    dfCoin['Date'] = pd.to_datetime(dfCoin['Date'])

    # Trier les données par date
    dfCoin = dfCoin.sort_values(by='Date')

    # Calcul des rendements quotidiens
    # pct_change mesure le pourcentage d'évolution entre une valeur et la précédente
    dfCoin['Returns'] = dfCoin['Close'].pct_change()

    # Calcul de la volatilité (écart-type des rendements sur 30 jours)
    # rolling permet de chosir une fenêtre de calcul
    # Ici on calcul l'ecart type des rendements sur 30 jours
    dfCoin['Volatility_30D'] = dfCoin['Returns'].rolling(window=30).std()

    # Ajout du lissage exponentiel pour la prévision des prix
    # le lissage exponentiel permet de lisser les variations de prix
    # le principe ce lissage est de calculer une moyenne exponentielle des prix
    # et donc de mettre plus de poids sur les prix récents
    dfCoin['EMA_10'] = dfCoin['Close'].ewm(span=10, adjust=False).mean()
    dfCoin['EMA_30'] = dfCoin['Close'].ewm(span=30, adjust=False).mean()

    # Calcul du seuil de forte volatilité
    volatility_threshold = dfCoin['Volatility_30D'].mean() + dfCoin['Volatility_30D'].std()
    dfCoin['High_Volatility'] = dfCoin['Volatility_30D'] > volatility_threshold

    # Supprimer les lignes avec des valeurs NaN 
    dfCoin_clean = dfCoin.dropna(subset=['Volatility_30D'])

    return dfCoin_clean;

"""
Fonction qui s'occupe de tracer les graphiques pour un bitcoin
"""
def plotVolatilite(dfCoin,nameAnalyse):
    volatility_threshold = dfCoin['Volatility_30D'].mean() + dfCoin['Volatility_30D'].std()

    # Tracer l'évolution du prix de clôture avec les moyennes mobiles exponentielles
    # EMA (Exponential Moving Average) 
    plt.figure(figsize=(12, 6))
    plt.plot(dfCoin['Date'], dfCoin['Close'], label='Prix de Clôture', color='blue', alpha=0.6)
    plt.plot(dfCoin['Date'], dfCoin['EMA_10'], label='EMA 10 jours', color='green', linestyle='dashed')
    plt.plot(dfCoin['Date'], dfCoin['EMA_30'], label='EMA 30 jours', color='red', linestyle='dashed')
    plt.xlabel('Date')
    plt.ylabel('Prix ($)')
    plt.title('Prix du '+nameAnalyse+' avec Moyennes Mobiles Exponentielles')
    plt.legend()
    plt.grid()
     # Sauvegarde les graphiques dans un dossier
    plt.savefig(os.path.join(cheminResultat, "MoyennesMobilesExp"+nameAnalyse+".png"), dpi=300)
    plt.show()

    # Tracer la volatilité avec indication des périodes de forte volatilité
    plt.figure(figsize=(12, 6))
    plt.plot(dfCoin['Date'], dfCoin['Volatility_30D'], label='Volatilité sur 30 jours', color='red')
    plt.axhline(y=volatility_threshold, color='black', linestyle='dashed', label='Seuil de Volatilité Élevée')

    # Mise en évidence des périodes de forte volatilité
    for i in range(1, len(dfCoin)):
        if dfCoin['High_Volatility'].iloc[i]:
            plt.axvspan(dfCoin['Date'].iloc[i-1], dfCoin['Date'].iloc[i], color='red', alpha=0.3)

    plt.xlabel('Date')
    plt.ylabel('Volatilité')
    plt.title('Volatilité du '+nameAnalyse+' avec Identification des Périodes à Risque')
    plt.legend()
    plt.grid()
     # Sauvegarde les graphiques dans un dossier
    plt.savefig(os.path.join(cheminResultat, "periodeRisque"+nameAnalyse+".png"), dpi=300)
    plt.show()


def resultatsGraphique():
    os.makedirs(cheminResultat, exist_ok=True)

"""
Fonction qui calcule les gains potentiels en fonction des périodes de volatilité
"""
def calculerGains(dfCoin, enveloppe):
    # Initialisation des variables
    capital = enveloppe
    en_position = False
    prix_achat = 0

    # Parcourir les données pour détecter les périodes de forte volatilité
    for i in range(1, len(dfCoin)):
        if dfCoin['High_Volatility'].iloc[i]:
            # Si on n'est pas en position, on achète
            if not en_position:
                prix_achat = dfCoin['Close'].iloc[i]
                en_position = True
        else:
            # Si on est en position et que la volatilité est faible, on vend
            if en_position:
                prix_vente = dfCoin['Close'].iloc[i]
                # Calcul du gain
                capital += (prix_vente - prix_achat) / prix_achat * enveloppe
                en_position = False

    # Si on est encore en position à la fin, on vend au dernier prix
    if en_position:
        prix_vente = dfCoin['Close'].iloc[-1]
        capital += (prix_vente - prix_achat) / prix_achat * enveloppe

    return capital

"""
Modification de la fonction principale pour inclure le calcul des gains
"""
def main():
    # Création du dossier pour les graphiques
    resultatsGraphique()
    # Lance un programme qui prend tous les CSV de différentes cryptos et qui les analyse
    csv_files = glob.glob("dataCrypto/*.csv")
    enveloppe = 1000  # Montant initial investi
    for file in csv_files:
        print(f"Analyse du fichier : {file}")
        file_name = os.path.basename(file)
        crypto_name = file_name.split('.')[0]
        dfCoin = pd.read_csv(file)
        dfCoin_clean = statsVolatilite(dfCoin)
        plotVolatilite(dfCoin_clean, crypto_name)
        gains = calculerGains(dfCoin_clean, enveloppe)
        print(f"Gains potentiels pour {crypto_name} avec une enveloppe de {enveloppe}€ : {gains:.2f}€")

# Lancement du programme pour analyse
main();


