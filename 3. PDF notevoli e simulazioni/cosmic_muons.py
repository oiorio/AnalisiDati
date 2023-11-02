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
area=100 # in cm^2
hours=48 # 2 giorni di acquisizione
t_data=hours*3600

muon_rate=I_0*omega*t_data*area

print(" il rate di muoni in "+str(hours)+" ore è: "+str(muon_rate))


#al di sopra di 10 GeV i muoni cosmici hanno una disctirbuzione in energia che è un esponenziale decrescente
#Consideriamo per semplicità un esponenziale decrescente con "vita media" 50 GeV: 
e1 = expon(scale=50,loc=10) #nota bene: in realtà dovremmo definirla solo al di sopra di 10 GeV, teniamo questa come prima approssimazione 
#(1/scale)*  e-((x-loc)/scale) --> scale è l'equivalente di 'tau', la vita media, loc è il punto di partenza

#generiamo ad esempio il numero di muoni cosmici previsto sopra:
energies = e1.rvs(size=int(muon_rate))
print(energies)

fig,ax= plt.subplots(1,1)
ax.hist(energies, density=True, bins='auto', histtype='stepfilled', alpha=0.2)
#plt.show()
plt.savefig("exponentials.png")

#Esercizio 1:
#Proviamo ora a generare un numero di eventi! Come dobbiamo procedere?

#Es. 1.1 totale
#hint:
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.poisson.html


import numpy as np
muon_prob = poisson(muon_rate)

ndatasets=100

#x= np.arange(muon_prob.ppf(0.01),muon_prob.ppf(0.99))
x= np.arange(muon_prob.ppf(1.0/ndatasets),muon_prob.ppf(1-1.0/ndatasets))#come estremi della PDF metto 1/(la dimensione del dataset):
#prendo essenzialmente i valori per cui mi aspetto al più 1 evento a sx e 1 evento a dx generando un numero di volte n=(dimensione del dataset)
ax.clear()
ax.plot(x, muon_prob.pmf(x), 'bo', ms=8, label='N muon probability ')
plt.savefig("poisson_prob.png")             

#Se vogliamo una distribuzione di dataset possiamo fare:

#N datasets:
n_datas = muon_prob.rvs(ndatasets)
ax.clear()
ax.hist(n_datas, density=True, bins='auto', histtype='stepfilled', alpha=0.2)
plt.savefig("poisson_sampled_prob.png")             


#Es. 1.2 considerando un'efficienza di rivelazione del 40%
#hint:
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.binom.html
#

efficiency=0.1

#metodo 1:
muon_prob_eff = poisson(muon_rate*efficiency)

n_datas_pois_eff = muon_prob_eff.rvs(ndatasets) #dataset generato con poissoniana "shiftata"

#metodo 2:
n_datas_eff = []

n_gen_pois=muon_prob.rvs()
n_gen_pois_eff= binom(n_gen_pois,efficiency).rvs()

print(n_gen_pois_eff)

#voglio generare un dataset con poissoniana e poi binomiale!

#prendo i dataset, ovvero i numeri di eventi, generati con la poissoniana:

for m in n_datas:
    binom_eff= binom(m,efficiency)    
    ngen = binom_eff.rvs()
    n_datas_eff.append(ngen)


ax.clear()
ax.hist(n_datas_pois_eff, density=True, bins='auto', histtype='stepfilled', alpha=0.2)
plt.savefig("poisson_eff_sampled_prob_v1.png")             

ax.hist(n_datas_eff, density=True, bins='auto', histtype='stepfilled', alpha=0.2)
plt.savefig("poisson_eff_sampled_prob_v2.png")             
#
#Esercizio 2: 

#importiamo le definizioni di particella:
from charged_particle import charged_particle as particle

#Es. 2.1 considerando tutti i muoni verticali, proviamo a definire un vettore di particelle!

n_particles=muon_prob_eff.rvs()
print(" the generated number of particles is: ",n_particles)

#2.1.2: consideriamo il passaggio attraverso un rivleatore generico.


#Dobbiamo decidere uno spettro di energia, ad esempio esponenziale
espectrum=e1.rvs(size=int(muon_prob_eff.rvs()))

#Mi aspetto che questo spettro non avrà alcuna differenza visibile con lo spettro in pt!
muon_particles=[]

m_muon=0.106#stiamo esprimendo in GeV
pz_1=[]
pz_2=[]
#Mettiamo una variabile per il livello di verbosità:
verbose=False #se è "True" allora facciamo dei printout --> possiamo passarla dall'esterno?
for energy in espectrum:
    #px,py,pz,e
    muon_e=particle(0,0,energy,e=energy,charge=-1)
    pz=math.sqrt(energy*energy-m_muon*m_muon)
    muon_e_with_mass=particle(0,0,pz,e=energy,charge=-1)
    if(verbose):print(energy,pz)
    
    pz_1.append(energy)
    pz_2.append(pz)

count,bins=np.histogram(espectrum)

ax.clear()
ax.hist(pz_1, bins=bins, density=False, histtype='stepfilled', alpha=0.2)
plt.savefig("muon_energy_distribution.png")             

ax.hist(pz_2,  bins=bins, density=False,  histtype='stepfilled', alpha=0.2)
plt.savefig("muon_pz_distribution.png")             
    
#Es. 2.2 se i muoni hanno una distribuzione angolare come cos2 (theta) cosa cambierà?
#Come posso considerare tale distribuzione?

#Dobbiamo trovare l'integrale, calcolare la cumulativa, invertirla etc

#Possiamo farlo "numericamente"?
#A. Root ce lo fa! --> vedere slides e poi facciamo
import ROOT
import math
import numpy as np

xMin=-0.5*math.pi
xMax=0.5*math.pi

#print(math.pi)
cos2 = ROOT.TF1("cos2theta","[0]*cos(x)*cos(x)+[1]+[2]*x",xMin,xMax)
cos2.SetParameter(0,1)
cos2.SetParameter(1,0)
cos2.SetParameter(2,0)
#cos2.SetParameters(1,0,0)#equivalente alle tre righe sopra
normalization=cos2.Integral(xMin,xMax)
print("l'integrale della funzione è: ",normalization)
cos2.SetParameter(0,1./normalization)
print("dopo aver normalizzato trovo: ",cos2.Integral(xMin,xMax))

cFunc= ROOT.TCanvas()
cFunc.Draw()
cos2.Draw()
cFunc.SaveAs("Cos2.png")

nevents=100000
histocos2 = ROOT.TH1F("histocos2","Histogram Sampled from cos2 distribution",100,xMin,xMax)
histocos2.FillRandom("cos2theta",nevents)
histocos2.Scale(1./nevents)#normalization to 1 term
histocos2.Scale(1./histocos2.GetBinWidth(1))#term for scaling the bin widht
histocos2.Draw("")
cFunc.SaveAs("Cos2_withhisto.png")

phif=ROOT.TF1("phi","[0]",0,2*math.pi)
phif.SetParameter(0,1/(2*math.pi))

px_3=[]
py_3=[]
pz_3=[]
e_3=[]

for energy in espectrum: 
    #px,py,pz,e
    theta = cos2.GetRandom()
    phi = phif.GetRandom()
    ptot=math.sqrt(energy*energy-m_muon*m_muon)
    st=math.sin(theta)
    ct=math.cos(theta)
    sp=math.sin(phi)
    cp=math.cos(phi)

    px=ptot*st*cp
    py=ptot*st*sp
    pz=ptot*ct
    muon_e_with_mass=particle(px=px,py=py,pz=pz,e=energy,charge=-1)
    if(verbose):print(energy,pz)
    
    px_3.append(px)
    py_3.append(py)
    pz_3.append(pz)

count,bins=np.histogram(px_3)
print(bins)
ax.clear()
ax.hist(px_3, bins=bins, density=False, histtype='stepfilled', alpha=0.2)
plt.savefig("muon_px_full.png")             

ax.clear()
ax.hist(py_3, bins=bins, density=False, histtype='stepfilled', alpha=0.2)
plt.savefig("muon_py_full.png")             

count,bins=np.histogram(pz_3)
ax.clear()
ax.hist(pz_3, bins=bins, density=False, histtype='stepfilled', alpha=0.2)
plt.savefig("muon_pz_full.png")             


#E se la mia energia venisse misurata con una risoluzione gaussiana dell'ordine di 10 GeV? Cosa succederebbe?
