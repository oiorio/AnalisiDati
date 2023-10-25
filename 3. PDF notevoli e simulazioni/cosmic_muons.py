#usiamo scipy.stats per le definizioni di distribuzione esponenziale e binomiale:
from scipy.stats import poisson,binom,expon
#importiamo matplotlib e math:
import matplotlib.pyplot as plt
import math
#prendiamo il flusso totale al livello del mare al di sopra di 10 GeV (https://www.diva-portal.org/smash/get/diva2:1597287/FULLTEXT01.pdf):
#il flusso integrale è ordine di 10-3 [cm-2 s-1 sr-1]:

I_0=0.001

#va integrato nell'angolo di zenith per i muoni!
#per ora consideriamo un angolo solido totale (2 pigreco, ma ci torneremo...)
#consideriamo un rivelatore a dimensione variabile, per esempio un quadrato di lato l = 10 cm

#scriviamo

omega=2*math.pi
area=100 # in cm
hours=48 # 2 giorni di acquisizione
t_data=hours*3600

muon_rate=I_0*omega*t_data

print(" il rate di muoni in "+str(hours)+" ore è: "+str(muon_rate))


#al di sopra di 10 GeV i muoni cosmici hanno una disctirbuzione in energia che è un esponenziale decrescente
#Consideriamo per semplicità un esponenziale decrescente con energia di dimezzamento 50 in GeV: 
e1 = expon(scale=50,loc=10) #nota bene: in realtà dovremmo definirla solo al di sopra di 10 GeV, teniamo questa come prima approssimazione 

#generiamo ad esempio 1000 muoni cosmici:
energies = e1.rvs(size=int(muon_rate))
fig,ax= plt.subplots(1,1)
ax.hist(energies, density=True, bins='auto', histtype='stepfilled', alpha=0.2)
plt.savefig("exponentials.png")

#Esercizio 1:
#Proviamo ora a generare un numero di eventi! Come dobbiamo procedere?

#Es. 1.1 totale
#hint:
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.poisson.html

#Es. 1.2 considerando un'efficienza di rivelazione del 40%
#hint:
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.binom.html

#Esercizio 2: 

#importiamo le definizioni di particella:
from charged_particle import charged_particle as particle

#Es. 2.1 considerando tutti i muoni verticali, proviamo a definire un vettore di particelle!

#Es. 2.2 se i muoni hanno una distribuzione angolare come cos2 (theta) cosa cambierà?
#Come posso considerare tale distribuzione?




