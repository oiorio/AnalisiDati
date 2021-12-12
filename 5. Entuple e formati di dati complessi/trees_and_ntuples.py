#!/usr/bin/env python
# coding: utf-8

# # Trees ed entuple

# ### Alcune definizioni:
# 
# - Evento : insieme di informazioni corrispondenti ad un avvenimento fisico
# 
# - Entupla : insieme di eventi in cui ognuno ha struttura tabulare
# 
# - Tree : insieme di eventi in cui ci sono oggetti "con struttura" più complessi, che in principio possono essere anch'essi ramificati.
# 
# 
# In genere useremo dei "Tree", anche se per la maggior parte dei casi non avremo bisogno solo della struttura tabulare.

# ## Files degli OPEN Data del CERN:
# 
# Prendiamo un campione di dati dagli OPEN Data del CERN (vedi anche CERN open data : http://opendata.cern.ch/search?page=1&size=20&experiment=CMS&subtype=Simulated&type=Dataset )
# 
# In particolare prendiamo una simulazione di eventi Drell-Yan (Z o fotoni ) che producono due leptoni nello stato finale. Documentazione: http://opendata.cern.ch/record/1395
# 
# Altro processo che considereremo: top quark-antiquark http://opendata.cern.ch/record/1359
# 
# Nota bene: i formati forniti tipicamente contengono molte più variabili di quelle che ci interessano - partiremo da un esempio con un certo grado di "predigestione"
# 
# ![drell-yan_leptons.png](attachment:drell-yan_leptons.png)

# ## Analisi degli open data:
# 
# Questi files sono stati processati di modo da ottenere un formato più compatto:
# 
# https://github.com/oiorio/AnalisiDati/tree/main/5.%20Entuple%20e%20formati%20di%20dati%20complessi

# In[1]:


import os,sys,subprocess as sp

# Mettiamo l'indirizzo in una stringahttps://github.com/oiorio/AnalisiDati/raw/main/5.%20Entuple%20e%20formati%20di%20dati%20complessi/DYJets.root
address_tree =  "https://github.com/oiorio/AnalisiDati/raw/main/5.%20Entuple%20e%20formati%20di%20dati%20complessi/DYJets.root"
#address_tree = "https://github.com/oiorio/AnalisiDati/raw/cf9599b45cd34f1aae71384a5b9b708f0e51a787/5.%20Entuple%20e%20formati%20di%20dati%20complessi/DYJets.root"

#prima controlliamo se il file è già in locale:
if os.path.exists("DYJets.root"):
    print("il File c'è già! Non sarà riscaricato.")
    download=[0,0]


# In[2]:


if not os.path.exists("DYJets.root") :
    #utilizzo subprocess, in particolare getstatusoutput
    download = sp.getstatusoutput("wget "+address_tree) 

    #fa 3 cose:
    #1 esegue il comando
    #2 salva lo status, se è andato a buon fine o se è fallito, e come 
    #3 salva l'output.

print(download[0]) #vediamo se è andato a buon fine!


# In[3]:


print(download[1]) #vediamo l'output


# In[4]:


# e ora vediamo l'output del comando ls usato per trovare tutti i fils che finiscono con root!
print(sp.getstatusoutput("ls -ltrha *.root" )[1]) 


# ### Cosa c'è nel tree?
# 
# Genericamente apriamo il file root con:
# 
#    root -l DYJets.root
#    
# In realtà faccio:

# In[5]:


import ROOT #sperando che funzioni...

inputFile = ROOT.TFile("DYJets.root","OPEN") #Così apro il file

print(inputFile.GetListOfKeys().Print())#Questo stampa le "chiavi" del file. 
#Come per una mappa o un dizionario ho un "item" in corrispondenza di una "key", in root ogni oggetto
#salvato in formato persistente ha una chiave


# In[6]:


#trovo un oggetto, posso chiamarlo con il punto come se fosse un metodo:
inputFile.trees


# In[7]:


#Scopro che è una "TDirectoryFile": posso di nuovo vedere il contenuto:
print(inputFile.trees.GetListOfKeys().Print())


# In[8]:


#Che a sua volta è:
inputFile.trees.events


# In[9]:


#Questo è un TTree!
#da PyRoot posso aprirlo come in C++

#Maniera alla C++
mytree = inputFile.Get("trees/events")

#Maniera alla python
mytree2 = inputFile.trees.events


# In[10]:


mytree2.Print()


# In[11]:


#Come faccio a prendere un componente di un tree?

#Maniera "alla python"

mytree.GetEntry(0)

nMuons = mytree.muontracks_size

print(nMuons)

mytree.GetEntry(1)

nMuons = mytree.muontracks_size

print(nMuons)

mytree.GetEntry(11)
print(mytree.muontracks_size)


# In[12]:


#Maniera alla C++
import array
nMuons_arr = array.array('i',[0])#1) creiamo un "contenitore" per la nostra variabile

mytree.SetBranchAddress("muontracks_size",nMuons_arr)

mytree.GetEntry(0)

print(nMuons_arr)

mytree.GetEntry(1)

print(nMuons_arr)


# ## Per visualizzare gli oggetti in un tree abbiamo diversi modi:
# 
# 1. In maniera "iterativa": iterando evento per evento e considerando in ognuno ciò che accade
# 
# 
# 2. In maniera "relazionale": sfruttando il formato dei dati, in cui ogni colonna è "legata" alle altre dello stesso evento globalmente.

# In[13]:


#Esempio 1: voglio disegnare l'energia mancante tutti gli eventi in cui ci sono 2 elettroni
c1 =ROOT.TCanvas()

#Metodo relazionale:
c1.Draw()
#mytree.Draw("jets_size","jets_pt[0]>50 && jets_pt[1]>30")
#mytree.Draw("jets_size","(muontracks_charge[0]==1 && muontracks_charge[1]==-1) || (muontracks_charge[0]==-1 && muontracks_charge[1]==1)")
mytree.Draw("met_pt>>h2(100,0,100)","electrons_size==2")

#si può fare la stessa cosa col metodo project


# In[14]:


#Metodo iterativo:
h1= ROOT.TH1F("met_pt_histo","met_pt",100,0,100)
for i in range(mytree.GetEntries()): 
    mytree.GetEntry(i)
    if(mytree.electrons_size==2):
        h1.Fill(mytree.met_pt[0])


#Se voglio proiettare in un istogramma una variabile che ottengo col metodo 1) posso usare Project
#mytree.Project("met_pt_histo","met_pt","electrons_size==2 && electrons_charge==1 ")        

c2=ROOT.TCanvas()
c2.Draw()
h1.Draw()


# In[15]:


#Vediamo i valori della carica:
mytree.Scan("electrons_size:electrons_charge","","",50)


# ## Domanda 0: Quale dei due metodi è più facile?
# <details>
#   <summary>Risposta 0</summary>
#   In questo caso ovviamente il metodo relazionale!
# </details>
# 
# 
# ## Domanda 1: perché i plot sono diversi?
# <details>
#   <summary>Risposta 1</summary>
#   Nel caso relazionale abbiamo lasciato a ROOT la scelta del binnaggio, nell'altro l'abbiamo scelto noi.
#   In realtà nel caso relazionale il bin
# </details>

# ## Domanda 3: e se volessi sapere "quando ci sono 2 elettroni/muoni con carica opposta"? 
# ## Oppure, ad esempio, quante coppie di elettroni di carica opposta ci sono?

# In[ ]:





# In[ ]:




