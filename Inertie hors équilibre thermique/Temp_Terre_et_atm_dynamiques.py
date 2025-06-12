import matplotlib.pyplot as plt
import numpy as np
from math import cos, sin, pi

#Constantes et paramètres
dt = 600 #Pas de temps
rho_terre = 1000 #Masse volumique de l'eau
rho_atmosphère = 1.2 #Masse volumique de l'atmosphère, en fonction de la concentration en les gazs
capa_atm = 1000
epaisseur_atm = 13000 #Epaisseur de l'atmosphère
Prof = 0.6 #Profondeur typique de variation de température de la terre sur une journée
sigma = 4.67*10**(-8) #Constante de Stefan-Boltzmann
pi = np.pi
puiss = np.array([1340, 0, 0])

def convertir(degres):
    """permet de convertir une valeur en degrés en radiant"""
    rad=(degres*2*pi)/360
    return rad

alpha = convertir(23.5) #angle Terre
R = 6371000 #rayon de la Terre

#albédo
glace = 0.60
eau = 0.10
neige = 0.80
desert = 0.35
foret = 0.20
terre = 0.15

def albedo(lat, lng):
    '''Retourne l'albedo d'une maille en fonction de sa latitude et de sa longitude'''

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

# Capacité thermique massique en J/kg.K
capa_glace = 2060
capa_eau = 4185
capa_neige = 2092
capa_desert = 835
capa_foret = 2400
capa_terre = 750

# Capacité thermique massique en fonction de la localisation
def capacite(lat, lng):
    if lat >= 65 or lat <= -65 :
        return capa_glace
    elif lng >= 160 or lng <= -140 :
        return capa_eau
    elif lng <= -120 and lng >= -140 and lat >= -65 and lat <= 50 :
        return capa_eau
    elif lng <= -80 and lng >= -120 and lat >= -65 and lat <= 20 :
        return capa_eau
    elif lng <= 140 and lng >= -60 and lat >= -65 and lat <= -30 :
        return capa_eau
    elif lng <= -60 and lng >= -80 and lat >= 10 and lat <= 40 :
        return capa_eau
    elif lng <= 0 and lng >= -60 and lat >= 30 and lat <= 65 :
        return capa_eau
    elif lng <= -20 and lng >= -60 and lat >= 10 and lat <= 30 :
        return capa_eau
    elif lng <= 10 and lng >= -60 and lat >= 0 and lat <= 10 :
        return capa_eau
    elif lng <= 10 and lng >= -40 and lat >= -30 and lat <= 0 :
        return capa_eau
    elif lng <= 120 and lng >= 40 and lat >= 10 and lat <= 20 :
        return capa_eau
    elif lng <= 100 and lng >= 40 and lat >= -30 and lat <= 10 :
        return capa_eau
    elif lng <= 120 and lng >= 100 and lat >= -30 and lat <= -10 :
        return capa_eau
    elif lng <= 140 and lng >= 120 and lat >= 0 and lat <= 30 :
        return capa_eau
    elif lng <= 160 and lng >= 140 and lat >= 0 and lat <= 60 :
        return capa_eau
    elif lng <= -60 and lng >= - 80 and lat<= 10 and lat >= 0 :
       return capa_foret
    elif lng <= -40 and lng >= - 80 and lat <= 0 and lat >= -30 :
        return capa_foret
    elif lng <= -60 and lng >= - 80 and lat <= -30 and lat >= -65 :
        return capa_foret
    elif lng <= 40 and lng >= - 20 and lat <= 20  and lat >= -10 :
        return capa_foret
    elif lng <= 140 and lng >= 100 and lat<= 40 and lat >= 30 :
        return capa_foret
    elif lng <= 120 and lng >= 100 and lat<= 30 and lat >= 0 :
        return capa_foret
    elif lng <= 160 and lng >= 100 and lat<= 0 and lat >= -10 :
        return capa_foret
    elif lng <= 40 and lng >= 10 and lat<= -10 and lat >= -30 :
        return capa_desert
    elif lng <= 60 and lng >= 0 and lat<= 40 and lat >= 20 :
        return capa_desert
    elif lng <= 160 and lng >= 120 and lat<= -10 and lat >= -30 :
        return capa_desert
    elif lng <= -80 and lng >= - 120 and lat<= 50 and lat >= 20 :
        return capa_terre
    elif lng <= 140 and lng >= 0 and lat<= 60 and lat >= 30 :
        return capa_terre
    elif lng <= 60 and lng >= 40 and lat<= 40 and lat >= 20 :
        return capa_terre
    elif lng <= 100 and lng >= 40 and lat<= 40 and lat >= 20 :
        return capa_terre
    else:
        return capa_neige

def B_point(j):
    '''Calcule angle entre l'inclinaison entre l'axe de rotation de la Terre autour d'elle même et celui autour du Soleil'''
    return alpha*cos(2*pi*j/365) #Le jour n°0 correspond ainsi au solstice d'été, le 21 juin

def dpuiss(lat, lng, h, j, puiss):
    '''Puissance reçu par une maille avec er la projection du vecteur de la base sphérique dans la base cartesienne'''
    B = B_point(j)

    er = np.array([cos(lng+((h - 8) * 2 * pi / 24)-pi/2) * sin(B + (pi / 2) - lat), sin(B + (pi / 2) - lat) * sin(lng+((h - 8) * 2 * pi / 24)-pi/2), cos((B + (pi / 2) - lat))])

    vec = np.dot(er, puiss)

    if vec <= 0 :
        return abs(vec)

    else :
        return 0

def Temp(lat, lng ):
    jour = 0
    liste_T = []
    liste_t = []
    T_T = 280
    T_atm = 255
    while (jour<1200):
        t = 0
        #Formule fonctionnant la nuit :
        while t < 84600 :
            h = t//3600
            liste_T.append(T_T)
            liste_t.append(t+jour*84600)
            dT_T = ((1- albedo(lat,lng))*dpuiss(lat,lng,h,jour,puiss)+sigma*(T_atm**4-T_T**4))*dt/(capacite(lat,lng)*rho_terre*Prof)
            dT_atm = sigma*(T_T**4-2*T_atm**4)*dt/(capa_atm*rho_atmosphère*epaisseur_atm)
            T_T = T_T + dT_T
            T_atm = T_atm + dT_atm
            t = t+dt
        jour = jour + 1

    fig, ax = plt.subplots()

    plt.plot(liste_t, liste_T)
    ax.set_xlabel('temps (s)', fontsize=15)
    ax.set_ylabel('Température à la surface (K)', fontsize=15)
    plt.show()

Temp(45,4)