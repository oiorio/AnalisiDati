#!/usr/bin/env python
# coding: utf-8

# # Esempio di notebook jupyter!
# 
# i notebook jupyter *(JUlia PYthon ad R)* sono un comodo strumento di scrittura interattiva di codice "web-based" 
# 
# Permettono di combinare in "blocchi" di testo e codice assieme in un ambiente interattivo.

# Si basa su un *kernel* in **Interactive Python (IPython)** che comunica con l'input-output.
# 
# ![ipy_kernel_and_terminal.png](attachment:ipy_kernel_and_terminal.png)

# Può agire da *wrapper* per l'esecuzione di altri linguaggi - oppure si possono aggiungere altri kernel in un linguaggio natio:
# 
# ![other_kernels.png](attachment:other_kernels.png)

# Reference:
# 
# https://jupyter.readthedocs.io/en/latest/projects/architecture/content-architecture.html

# ## Piccola nota sul formato markdown (.md):
# 
# è un formato di documentazione web-based, che permette di scrivere in maniera agile all'interno di git o notebooks 
# 
#     posso scrivere degli esempi di codice...
# 
# - fare una lista di items ...
# 
# 1. volendo anche numerata!
# 
# Posso aggiungere delle **estensioni custom** - e tanto altro ancora!
# 
# Una documentazione molto chiara con esempi si trova qui:
# 
# https://markdown-it.github.io/
# 

# ## Python e IPython
# 
# - IPython è un interpete "interattivo" alternativo a quello standard di python da linea di comando.
# 
# - Python è concepito come un linguaggio interpretato, in realtà nella sua versione più comune preoduce dei files .pyc che sono delle "caches" in bytecode compilate, che vengono riutilizzate all'occorrenza girando il python file.
# 
# Nota: La distinzione tra interpretato e compilato è da molti considerata "old fashioned", perché molti linguaggi presentano un'implementazione compilata, interpretata, o both.
# 

# ## Come lo usiamo?
# 
# Quello che scriviamo come notebook è in IPython natio, ma l'interfaccia è in python <==> possiamo utilizzarlo come se fosse un file di python dal vivo - perfetto per la prototipazione!
# 
# ## Nota bene: tutto quello fatto di seguito può essere riprodotto esattamente su python!
# 
# In tal caso dovrete aprire uno script python, editarlo, ed eseguirlo come
# 
# 
# 

# In[19]:


#Iniziamo quindi dall'importare delle librerie di python
import os,sys


# In[20]:


#OS permette di interagire col sistema operativo, ad esempio :
os.system("pwd")

os.system("echo '\nMi restituirà il risultato del comando come eseguito da bash!\n'")

os.system("echo 'Ad esempio, il path dei comandi è: \n'$PATH ")


# In[21]:


#Sys, d'altro canto, è 

print (sys.path)


# In[22]:


#Se avete seguito le istruzioni per l'installazione, ad es. su , dovrebbe essere possibile
import ROOT


# In[24]:


# Facciamo alcuni esempi di base per reiscaldarci:


# In[33]:


h1 = ROOT.TH1F("h1_esempio","Istogramma d'esempio",100,-10,10)
f1 = ROOT.TF1("f1_esempio","gaus",-10,10)
f1.SetParameters(10,1,5)

h1.FillRandom("f1_esempio",1000)

c1 = ROOT.TCanvas()
c1.Draw()

h1.Draw()


# In[44]:


c1.Draw()

for i in range(0,200):
    h1.FillRandom("f1_esempio",1)
h1.DrawNormalized()
h1.Fit(f1,"S")


# # Ci siamo?
# 
# ### Nota bene: se jupyter non funziona, possiamo equivalentemente usare python!
# 
# ### Se vogliamo convertire il file in python "puro" per compilarlo o altro, possiamo farlo - da download as:
# 
# ![salvare_python_1-2.JPG](attachment:salvare_python_1-2.JPG)
# 
# ### E scegliando .py come estensione dal menu a tendina.

# In[ ]:





# In[ ]:




