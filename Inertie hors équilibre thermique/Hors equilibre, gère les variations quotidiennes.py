import matplotlib.pyplot as plt
import numpy as np

Ps = 1000
A = 0.4 #Albedo de la Terre dans la longueur d'onde qu'elle émet, c'est à dire les infrarouges
C_eau = 4185
C_sable = 835
C = C_eau*0.7 + C_sable*0.3
Capacite_terre = 3300
profondeur = 0.5
rho_eau = 1000
T = 290
t = 0 #Heure du coucher du soleil, pris comme référence
dt = 1
sigma =5.67*10**(-8) #Constante de Stefan-Boltzmann
Beta = 0.5 #Proportion de ce qui est renvoyé dans la terre par l'atmosphère, dans le rayonnemment infrarouge
liste_T = []
liste_t = []
pi = np.pi


def P_rec(t):
    while t >86400:
        t = t - 86400
    if t < 28800:
        return 0
    if (t > 28800 and t < 72000):
        return(Ps*np.sin((t-28800)*pi/43200))
    else :
        return 0

#Formule fonctionnant la nuit :
while t < 30*84600 :
    liste_T.append(T)
    liste_t.append(t)
    T = T + dt*(1-A)*(1+A*Beta*(1-A))*P_rec(t)/(C*rho_eau*profondeur) - T**4*sigma*dt*(1-(1-A)*Beta)/(C*rho_eau*profondeur)
    t = t+dt

fig, ax = plt.subplots()

plt.plot(liste_t, liste_T)
ax.set_xlabel('temps (s)', fontsize=15)
ax.set_ylabel('Température à la surface (K)', fontsize=15)
plt.show()


