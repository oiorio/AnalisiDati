import ROOT
import sys,os
import numpy as np
sys.path.append(os.getcwd()+("/python")) #aggiungiamo il path di python, dove metteremo le librerie
print(sys.path)


#Parte 1: costruiamo il modello dal file di configurazione
from utilities import getModel #carichiamo la funzione model che usiamo per prendere i modelli  
fg,fe,fge=getModel("models/model_3.txt") #vedere getModel: restituisce funzione gaussiana, esponenziale e somma

#Nota: se abbiamo usato una notazione consistente
#dovremmo poter scegliere l'analisi variando solo il numero "3"
#che sta prima dell'estensione del file, qui e nei vari punti dove è necessario

#Parte 2: usiamo le utilities di root per il fit
print(fge)
fileHistos=ROOT.TFile("LLFile.root")#prendiamo il file creato prima

h3=fileHistos.Get("data_exercise_Likelihood_3_txt")
h3.Fit(fge.GetName())

c1=ROOT.TCanvas()
c1.Draw()
h3.Draw()
c1.SaveAs("fitGaussExpo1.png")

#Parte 3: facciamo il likelihood scan
from utilities import txtToArray 

#otteniamo il vettore "unbinned": ho bisogno di riprendere il file di dati. Una copia è in "models"
x_array=txtToArray("models/exercise_Likelihood_3.txt")
print (x_array)

#otteniamo il vettore "binned"
xbinned_array= np.array([ h3.GetBinContent(i) for i in range(1,h3.GetNbinsX()+1)])
print (xbinned_array)


#Esercizio:
#Usando le funzioni fge.Eval(x) e fge.Integral(xmin,xmax)
#proviamo a valutare la likelihood
#in funzione del numero di eventi di segnale e fondo

ntotal=len(x_array)
import math
lnns=[]
lnn=0
lik=1.0
hlnn=ROOT.TH1F("hlnn","hlnn",ntotal,0,ntotal) 

for s in range(0,ntotal):
    lnn=0
    fge.SetParameter(3,s/ntotal)
    fge.SetParameter(4,(ntotal-s)/ntotal)
    for x in x_array:
        lik=lik*fge.Eval(x)
        lnn_xi=-2*math.log(fge.Eval(x))
        lnn=lnn + lnn_xi
    lnns.append(lnn)
    hlnn.SetBinContent(s,lnn)
    smin=np.min(np.array(lnns))


hlnn.Draw()
c1.Draw()
c1.SaveAs("lnn_shape.png")

fout=ROOT.TFile("zoomfile.root","RECREATE")
hlnn.Write()
fout.Close()
