# Capacité thermique massique en J/kg.K
glace = 2060
eau = 4185
neige = 2092
desert = 830000
foret = 2400
terre = 750

## Capacité thermique massique en fonction de la localisation
def capacite(lat, lng):
    if lat >= 65 or lat <= -65 :
        return glace
    elif lng >= 160 or lng <= -140 :
        return eau
    elif lng <= -120 and lng >= -140 and lat >= -65 and lat <= 50 :
        return eau
    elif lng <= -80 and lng >= -120 and lat >= -65 and lat <= 20 :
        return eau
    elif lng <= 140 and lng >= -60 and lat >= -65 and lat <= -30 :
        return eau
    elif lng <= -60 and lng >= -80 and lat >= 10 and lat <= 40 :
        return eau
    elif lng <= 0 and lng >= -60 and lat >= 30 and lat <= 65 :
        return eau
    elif lng <= -20 and lng >= -60 and lat >= 10 and lat <= 30 :
        return eau
    elif lng <= 10 and lng >= -60 and lat >= 0 and lat <= 10 :
        return eau
    elif lng <= 10 and lng >= -40 and lat >= -30 and lat <= 0 :
        return eau
    elif lng <= 120 and lng >= 40 and lat >= 10 and lat <= 20 :
        return eau
    elif lng <= 100 and lng >= 40 and lat >= -30 and lat <= 10 :
        return eau
    elif lng <= 120 and lng >= 100 and lat >= -30 and lat <= -10 :
        return eau
    elif lng <= 140 and lng >= 120 and lat >= 0 and lat <= 30 :
        return eau
    elif lng <= 160 and lng >= 140 and lat >= 0 and lat <= 60 :
        return eau
    elif lng <= -60 and lng >= - 80 and lat<= 10 and lat >= 0 :
       return foret
    elif lng <= -40 and lng >= - 80 and lat <= 0 and lat >= -30 :
        return foret
    elif lng <= -60 and lng >= - 80 and lat <= -30 and lat >= -65 :
        return foret
    elif lng <= 40 and lng >= - 20 and lat <= 20  and lat >= -10 :
        return foret
    elif lng <= 140 and lng >= 100 and lat<= 40 and lat >= 30 :
        return foret
    elif lng <= 120 and lng >= 100 and lat<= 30 and lat >= 0 :
        return foret
    elif lng <= 160 and lng >= 100 and lat<= 0 and lat >= -10 :
        return foret
    elif lng <= 40 and lng >= 10 and lat<= -10 and lat >= -30 :
        return desert
    elif lng <= 60 and lng >= 0 and lat<= 40 and lat >= 20 :
        return desert
    elif lng <= 160 and lng >= 120 and lat<= -10 and lat >= -30 :
        return desert
    elif lng <= -80 and lng >= - 120 and lat<= 50 and lat >= 20 :
        return terre
    elif lng <= 140 and lng >= 0 and lat<= 60 and lat >= 30 :
        return terre
    elif lng <= 60 and lng >= 40 and lat<= 40 and lat >= 20 :
        return terre
    elif lng <= 100 and lng >= 40 and lat<= 40 and lat >= 20 :
        return terre
    else:
        return neige