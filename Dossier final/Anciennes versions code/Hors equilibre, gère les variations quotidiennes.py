import matplotlib.pyplot as plt
import numpy as np
from math import cos, sin, pi

Ps = 1000
A = 0.4 #Albedo de la Terre dans la longueur d'onde qu'elle émet, c'est à dire les infrarouges
C_eau = 4185
C_sable = 835
C = C_eau*0.7 + C_sable*0.3
Capacite_terre = 3300
profondeur = 0.2
rho_eau = 1000
T = 290
t = 0 #Heure du coucher du soleil, pris comme référence
dt = 10
sigma =5.67*10**(-8) #Constante de Stefan-Boltzmann
Beta = 0.5 #Proportion de ce qui est renvoyé dans la terre par l'atmosphère, dans le rayonnemment infrarouge
liste_T = []
liste_t = []
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

def B_point(j):
    '''Calcule angle entre l'inclinaison entre l'axe de rotation de la Terre autour d'elle même et celui autour du Soleil'''
    return alpha*cos(2*pi*j/365)

def dpuiss(lat, lng, h, j, puiss):
    '''Puissance reçu par une maille avec er la projection du vecteur de la base sphérique dans la base cartesienne'''
    B = B_point(j)

    er = np.array([cos(lng+((h - 8) * 2 * pi / 24)-pi/2) * sin(B + (pi / 2) - lat), sin(B + (pi / 2) - lat) * sin(lng+((h - 8) * 2 * pi / 24)-pi/2), cos((B + (pi / 2) - lat))])

    vec = np.dot(er, puiss)

    if vec <= 0 :
        return abs(vec)

    else :
        return 0


def puiss_sol(lat, lng, h, j, puiss):
    '''Calcule la puissance totale reçue par la pacelle de sol après les différents rebonds liés à l'effet de serre, mais sans prendre en compte la réémission propre au corps noir qu'est la Terre. On considère ici que l'albedo de l'atmosphère      est constant, égal à 0.8. On somme toutes les réfléxions et on a mis ici la somme de la série, qui est une série géométrique de raison strictement inférieure à 1.'''
    p = (0.8*(1-albedo(lat,lng))*dpuiss (lat, lng, h, j, puiss))/(1-0.2*albedo(lat,lng))
    return p

def p_sol(lat, lng, h, j, puiss):
    '''Calcule la puissance reçue par la Terre après réémission des infrarouges liées au corps noir, en supposant que la Terre est un système thermodynamique à l'équilibre, elle re-reçoit donc une partie de ce qu'elle a ré-émis.'''
    Precue = puiss_sol(lat, lng, h, j, puiss)
    p = (Precue*(1.2-0.4*albedo(lat,lng)))/(1-0.2*albedo(lat,lng))
    return p


def Temp(lat, lng ):
    jour = 0
    liste_T = []
    liste_t = []
    T = 290
    while (jour<730):
        t = 0
        #Formule fonctionnant la nuit :
        while t < 84600 :
            h = t//3600
            liste_T.append(T)
            liste_t.append(t+jour*84600)
            T = T + dt*(1-A)*(1+A*Beta*(1-A))*p_sol(lat, lng,h, jour, puiss)/(C*rho_eau*profondeur) - T**4*sigma*dt*(1-(1-A)*Beta)/(C*rho_eau*profondeur)
            t = t+dt
        jour = jour + 1

    fig, ax = plt.subplots()

    plt.plot(liste_t, liste_T)
    ax.set_xlabel('temps (s)', fontsize=15)
    ax.set_ylabel('Température à la surface (K)', fontsize=15)
    plt.show()


Temp(45,4)