#Cette librairie propose une convention pour le nom des puissances surfaciques considérées, mais n'a pas vocation à être réutilisée telle quelle.
# conventions:
# lat: float (radian), 0 is at equator, -pi/2 is at south pole, and +pi/2 is at north pole
# long: float (radian), 0 is at greenwich meridiant
# t: float (s), 0 is at 00:00 (greenwich time) january 1, 365*24*60*60 is at the end of the year, (maybe use 365.25? no idea what is best, or maybe use UTC ?)


import numpy as np

P0 = 1360  # W/m² – zenith irradiance at the top of the atmosphere
PHI = 0.409  # precession angle rad  (23.45 deg)
SIGMA = 5.67e-8  # W/m²K⁴ – Stefan-Boltzmann constant

# Capacités thermiques (constantes)
capa_glace = 2060
capa_eau = 4185
capa_neige = 2092
capa_desert = 835
capa_foret = 2400
capa_terre = 750

#Fonctions qui servent à déterminer des constantes

def capacite(lat: float, lng: float, t: float = 0):  '''->float'''
    """Capacité thermique massique en fonction de la localisation"""
    if lat >= 65 or lat <= -65:
        return capa_glace
    elif lng >= 160 or lng <= -140:
        return capa_eau
    elif lng <= -120 and lng >= -140 and lat >= -65 and lat <= 50:
        return capa_eau
    elif lng <= -80 and lng >= -120 and lat >= -65 and lat <= 20:
        return capa_eau
    elif lng <= 140 and lng >= -60 and lat >= -65 and lat <= -30:
        return capa_eau
    elif lng <= -60 and lng >= -80 and lat >= 10 and lat <= 40:
        return capa_eau
    elif lng <= 0 and lng >= -60 and lat >= 30 and lat <= 65:
        return capa_eau
    elif lng <= -20 and lng >= -60 and lat >= 10 and lat <= 30:
        return capa_eau
    elif lng <= 10 and lng >= -60 and lat >= 0 and lat <= 10:
        return capa_eau
    elif lng <= 10 and lng >= -40 and lat >= -30 and lat <= 0:
        return capa_eau
    elif lng <= 120 and lng >= 40 and lat >= 10 and lat <= 20:
        return capa_eau
    elif lng <= 100 and lng >= 40 and lat >= -30 and lat <= 10:
        return capa_eau
    elif lng <= 120 and lng >= 100 and lat >= -30 and lat <= -10:
        return capa_eau
    elif lng <= 140 and lng >= 120 and lat >= 0 and lat <= 30:
        return capa_eau
    elif lng <= 160 and lng >= 140 and lat >= 0 and lat <= 60:
        return capa_eau
    elif lng <= -60 and lng >= -80 and lat <= 10 and lat >= 0:
        return capa_foret
    elif lng <= -40 and lng >= -80 and lat <= 0 and lat >= -30:
        return capa_foret
    elif lng <= -60 and lng >= -80 and lat <= -30 and lat >= -65:
        return capa_foret
    elif lng <= 40 and lng >= -20 and lat <= 20 and lat >= -10:
        return capa_foret
    elif lng <= 140 and lng >= 100 and lat <= 40 and lat >= 30:
        return capa_foret
    elif lng <= 120 and lng >= 100 and lat <= 30 and lat >= 0:
        return capa_foret
    elif lng <= 160 and lng >= 100 and lat <= 0 and lat >= -10:
        return capa_foret
    elif lng <= 40 and lng >= 10 and lat <= -10 and lat >= -30:
        return capa_desert
    elif lng <= 60 and lng >= 0 and lat <= 40 and lat >= 20:
        return capa_desert
    elif lng <= 160 and lng >= 120 and lat <= -10 and lat >= -30:
        return capa_desert
    elif lng <= -80 and lng >= -120 and lat <= 50 and lat >= 20:
        return capa_terre
    elif lng <= 140 and lng >= 0 and lat <= 60 and lat >= 30:
        return capa_terre
    elif lng <= 60 and lng >= 40 and lat <= 40 and lat >= 20:
        return capa_terre
    elif lng <= 100 and lng >= 40 and lat <= 40 and lat >= 20:
        return capa_terre
    else:
        return capa_neige





def P_inc_solar(lat:float, lng:float, t:float): '''->float'''
    puiss = np.array([1340, 0, 0])
    '''Puissance reçu par une maille avec er la projection du vecteur de la base sphérique dans la base cartesienne'''
    # Calcul du jour et de l'heure à partir du temps t
    j = t // 86400  # Jour (nombre entier de jours écoulés)
    h = (t % 86400) / 3600  # Heure dans la journée courante

    B = B_point(t)

    er = np.array([cos(lng+((h - 8) * 2 * pi / 24)-pi/2) * sin(B + (pi / 2) - lat), sin(B + (pi / 2) - lat) * sin(lng+((h - 8) * 2 * pi / 24)-pi/2), cos((B + (pi / 2) - lat))])

    vec = np.dot(er, puiss)

    if vec <= 0 :
        return abs(vec)

    else :
        return 0


# Surface
def P_abs_surf_solar(lat: float, long: float, t: float, Pinc: float): '''->float''' ##puissance absorbée par le sol
    AbsSurf = albedo(lat,lng,t)
    return AbsSurf * Pinc


def P_em_surf_thermal(lat: float, long: float, t: float, T: float):'''->float''' ##puissance émise par le sol dans les infrarouges
    return SIGMA * (T**4)


def P_em_surf_conv(lat: float, long: float, t: float): ##pas existante/ en reflexion
    return 0


def P_em_surf_evap(lat: float, long: float, t: float): ##pas existante
    return 0


# atmosphere
def P_abs_atm_solar(lat: float, long: float, t: float, Pinc: float): ## on considère l'amosphere transparente au visible
    return 0


def P_abs_atm_thermal(lat: float, long: float, t: float, T_T: float): ## puissance abrobé par l'atmosphère dans l'infrarouge
    epsilon = 0.71 #Proportions des rayons infrarouges qui sont effectivement absorbés par l'atmosphère, on considère que le reste est perdu dans le vide intersidéral
    return (P_em_surf_thermal(lat,lng,t,T_T)*epsilon)


def P_em_atm_thermal_up(lat: float, long: float, t: float, T_atm:float):  ## puissance emise par atmosphère domaine infrarouge dans le vide intersidéral
    return SIGMA * (T_atm**4)


def P_em_atm_thermal_down(lat: float, long: float, t: float, T_atm:float): ## puissance emise par atmosphère domaine infrarouge vers l'intérieur de la Terre
    return SIGMA * (T_atm**4)
