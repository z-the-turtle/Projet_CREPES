import matplotlib.pyplot as plt

Ps = 1361
A = 0.5 #Albedo de la Terre dans la longueur d'onde qu'elle émet, c'est à dire les infrarouges
C_eau = 4185
C_sable = 835
C = C_eau*0.6 + C_sable*0.4
Capacite_terre = 3300
profondeur = 0.1
rho_eau = 1000
T = 295
t = 0 #Heure du coucher du soleil, pris comme référence
dt = 0.05
sigma =5.67*10**(-8) #Constante de Stefan-Boltzmann
Beta = 0.3 #Proportion de ce qui est renvoyé dans la terre par l'atmosphère, dans le rayonnemment infrarouge
liste_T = []
liste_t = []

Terme_source = Ps*(1-A)/4 #A ne prendre en compte que de jour, de nuit, il n'y a pas de soleil !

#Formule fonctionnant la nuit :
while t < 36000:
    liste_T.append(T)
    liste_t.append(t)
    T = T - T**4*sigma*dt*(1-(1-A)*Beta)/(C*rho_eau*profondeur)
    t = t+dt

plt.plot(liste_t, liste_T)
plt.show()