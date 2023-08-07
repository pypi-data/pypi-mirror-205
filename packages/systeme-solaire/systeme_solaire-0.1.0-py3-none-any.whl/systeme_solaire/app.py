"""Exemple d'objet terre en utilisant l'api astroquery"""
from datetime import datetime, timedelta
from astroquery.jplhorizons import Horizons

# Spécifiez les dates pour lesquelles vous voulez récupérer les coordonnées
dates = {'start': (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d'),
         'stop': (datetime.utcnow() + timedelta(days=30)).strftime('%Y-%m-%d'),
         'step': '1d'}

# Créez un objet Horizons pour la Terre
earth = Horizons(id='399', location='@sun', epochs=dates)


# Récupérez les coordonnées de la Terre pour les dates spécifiées
ephemeris = earth.ephemerides()

# Parcourez les coordonnées récupérées pour chaque jour
for eph in ephemeris:
    date = eph['datetime_str']
    ra, dec, distance = eph['RA'], eph['DEC'], eph['delta']
    print(f"Le {date}, la position de la Terre est (RA, DEC) = " +
          "({ra}, {dec}), à une distance de {distance} UA du Soleil.")
