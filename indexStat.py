"""
Author:Yanis Ponthou & Lucas Desperrois
Programme qui s'occupe de l'analyse statistique de la volatilité de cryptoMonnaies
pour prendre des décisions d'achat
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
    dfCoin['evolution'] = dfCoin['Close'].pct_change()
    # Calcul de la volatilité (écart-type des rendements sur 30 jours)
    # rolling permet de chosir une fenêtre de calcul
    # Ici on calcul l'ecart type des rendements sur 30 jours
    dfCoin['Volatility_30D'] = dfCoin['evolution'].rolling(window=30).std()
    # Ajout du lissage exponentiel pour la prévision des prix
    # le lissage exponentiel permet de lisser les variations de prix
    # le principe ce lissage est de calculer une moyenne exponentielle des prix
    # et donc de mettre plus de poids sur les prix récents
    dfCoin['EMA_10'] = dfCoin['Close'].ewm(span=10, adjust=False).mean()
    dfCoin['EMA_30'] = dfCoin['Close'].ewm(span=30, adjust=False).mean()
    # Calcul du seuil de forte volatilité
    seuilVolatilite = dfCoin['Volatility_30D'].mean() + dfCoin['Volatility_30D'].std()
    dfCoin['High_Volatility'] = dfCoin['Volatility_30D'] > seuilVolatilite
    dfCoin_clean = dfCoin.dropna(subset=['Volatility_30D'])
    return dfCoin_clean;

"""
Fonction qui s'occupe de tracer les graphiques pour un bitcoin
"""
def plotVolatilite(dfCoin,nameAnalyse):
    seuilVolatilite =  dfCoin['Volatility_30D'].std() +dfCoin['Volatility_30D'].mean()

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
    plt.savefig(os.path.join(cheminResultat, "MoyennesMobilesExp"+nameAnalyse+".png"), dpi=300)
    plt.show()

    # Tracer la volatilité avec indication des périodes de forte volatilité
    plt.figure(figsize=(12, 6))
    plt.plot(dfCoin['Date'], dfCoin['Volatility_30D'], label='Volatilité sur 30 jours', color='red')
    plt.axhline(y=seuilVolatilite, color='black', linestyle='dashed', label='Seuil de Volatilité Élevée')

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
    # Calcul du seuil de forte volatilité
    seuilVolatilite =  dfCoin['Volatility_30D'].std() + dfCoin['Volatility_30D'].mean() 
    for i in range(1, len(dfCoin)):
        # Si la volatilité est élevée (au-dessus du seuil)
        if dfCoin['Volatility_30D'].iloc[i] > seuilVolatilite:
            # Si on est en position, on vend
            if en_position and dfCoin['Close'].iloc[i] > prix_achat:
                prix_vente = dfCoin['Close'].iloc[i]
                capital += (prix_vente - prix_achat) / prix_achat * capital
                print(f"Vente à {prix_vente:.2f}€ (Volatilité élevée) - Capital : {capital:.2f}€")
                en_position = False
        else:
            # Si la volatilité est faible (en dessous du seuil)
            if not en_position:
                prix_achat = dfCoin['Close'].iloc[i]
                print(f"Achat à {prix_achat:.2f}€ (Volatilité faible)")
                en_position = True

    # Si on est encore en position à la fin, on vend au dernier prix
    if en_position:
        prix_vente = dfCoin['Close'].iloc[-1]
        capital += (prix_vente - prix_achat) / prix_achat * capital
        print(f"Vente finale à {prix_vente:.2f}€ - Capital : {capital:.2f}€")

    return capital - enveloppe



"""
Fonction qui s'occupe de la présence du dossier crypto et de csv présent
dans celui-ci
"""
def compterFichiers():
    dossier = "dataCrypto"
    if not os.path.exists(dossier):
        print(f"Le dossier '{dossier}' n'existe pas.")
        return []
    listeFichiers = glob.glob("dataCrypto/*.csv")
    if not listeFichiers:
        print(f"Aucun fichier CSV trouvé dans le dossier '{dossier}'.")
    return listeFichiers
    

"""
Fonction qui s'occupe de vérifier la présence des colonnes nécessaires aux calculs
"""
def checkColumns(file):
    df = pd.read_csv(file)
    list_of_column_names = list(df.columns) 
    if("Close" not in list_of_column_names or "Date" not in list_of_column_names):
        print(f"le fichier {file} ne contient pas les colonnes obligatoire pour analyse : Date et Close")
        return False
    else:
        return True
    
def generer_scenarios_marche(df, horizon=10, window_slope=30):
    """
    Crée 3 scénarios (optimiste, neutre, pessimiste) sur 'horizon' jours.
    - On estime une pente moyenne sur la période 'window_slope' jours.
    - On ajoute un ajustement basé sur la volatilité moyenne (calculée sur la fin).
    """
    if len(df) < window_slope:
        print(f"Pas assez de données pour calculer la pente sur {window_slope} jours.")
        return None

    last_price = df['Close'].iloc[-1]

    # Pente sur 'window_slope' jours
    start_price = df['Close'].iloc[-window_slope]
    slope = (last_price - start_price) / window_slope

    # On veut la volatilité moyenne sur la même fenêtre
    # Si Volatility_30D est calculée, on la prend, sinon on refait un calcul "manuel".
    if 'Volatility_30D' in df.columns and df['Volatility_30D'].iloc[-window_slope:].notna().any():
        avg_vol = df['Volatility_30D'].iloc[-window_slope:].mean()
    else:
        # Calcul "manuel" de la volatilité si on n'a rien dans la colonne
        # On prend l'écart-type des 30 derniers rendements
        if len(df) >= 30:
            avg_vol = df['evolution'].iloc[-30:].std()
        else:
            avg_vol = 0.0

    print(f"Volatilité moyenne sur la fenêtre: {avg_vol:.8f}")

    price_opt = last_price
    price_neutre = last_price
    price_pess = last_price

    scenarios = {
        'optimiste': [],
        'neutre': [],
        'pessimiste': []
    }

    facteur_opt = 1.2  
    facteur_pess = 0.8 

    for day in range(1, horizon+1):
        # Scenario optimiste
        price_opt += slope * facteur_opt + 0.1 * avg_vol
        scenarios['optimiste'].append(price_opt)

        # Scenario neutre
        price_neutre += slope
        scenarios['neutre'].append(price_neutre)

        # Scenario pessimiste
        price_pess += slope * facteur_pess - 0.1 * avg_vol
        scenarios['pessimiste'].append(price_pess)

    return scenarios


"""
Fonction qui s'occupe de lancer l'objectif du projet  :
Identifier les périodes de volatibilité faible ou forte pour appliquer
une stratégie d'investissement
"""
def main(enveloppe):
    # Création du dossier pour les graphiques
    resultatsGraphique()
    csv_files = compterFichiers()
    if(csv_files!=[]):
        for file in csv_files:
            if(not checkColumns(file)):
                print("Fichier ignoré");
                continue
            print(f"Analyse du fichier : {file}")
            file_name = os.path.basename(file)
            crypto_name = file_name.split('.')[0]
            dfCoin = pd.read_csv(file)
            dfCoin_clean = statsVolatilite(dfCoin)
            plotVolatilite(dfCoin_clean, crypto_name)
            gains = calculerGains(dfCoin_clean, enveloppe)
            print(f"Gains potentiels pour {crypto_name} avec une enveloppe de {enveloppe}€ : {gains:.2f}€ sur la periode  du "+str(dfCoin_clean['Date'].iloc[0])+" au "+str(dfCoin_clean['Date'].iloc[-1]))
            
            # ---------------------------------------------------------------
            # GÉNÉRATION DE SCÉNARIOS DE MARCHÉ + AFFICHAGE
            # ---------------------------------------------------------------
            
            print("\n=== Génération de Scénarios de Marché ===")
            scenarios = generer_scenarios_marche(dfCoin_clean, horizon=10, window_slope=30)
            if scenarios:
                last_price = dfCoin_clean['Close'].iloc[-1]
                print(f"Prix de départ: {last_price:.6f} (dernier jour réel)")

                # --- Optimiste
                final_opt = scenarios['optimiste'][-1]
                diff_opt = last_price - final_opt
                if diff_opt > 0:
                    print(f"Scénario optimiste: tombe à {final_opt:.6f} (J+10) -> baisse de ~{diff_opt:.6f}")
                else:
                    hausse_opt = abs(diff_opt)
                    print(f"Scénario optimiste: monte à {final_opt:.6f} (J+10) -> hausse de ~{hausse_opt:.6f}")

                # --- Neutre
                final_neutre = scenarios['neutre'][-1]
                diff_neutre = last_price - final_neutre
                if diff_neutre > 0:
                    print(f"Scénario neutre   : tombe à {final_neutre:.6f} (J+10) -> baisse de ~{diff_neutre:.6f}")
                else:
                    hausse_neutre = abs(diff_neutre)
                    print(f"Scénario neutre   : monte à {final_neutre:.6f} (J+10) -> hausse de ~{hausse_neutre:.6f}")

                # --- Pessimiste
                final_pess = scenarios['pessimiste'][-1]
                diff_pess = last_price - final_pess
                if diff_pess > 0:
                    print(f"Scénario pessimist: tombe à {final_pess:.6f} (J+10) -> baisse de ~{diff_pess:.6f}")
                else:
                    hausse_pess = abs(diff_pess)
                    print(f"Scénario pessimist: monte à {final_pess:.6f} (J+10) -> hausse de ~{hausse_pess:.6f}")
            else:
                print("Impossible de générer les scénarios (pas assez de données).")

            print("-------------------------------------------------\n")
    else:
        print("Le Programme s'est arrêté suite à une condition non respecté pour lancer le code python.")
# Lancement du programme pour analyse avec 1000 euros
main(1000);


