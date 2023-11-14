import ROOT
import sys,os
import numpy as np
sys.path.append(os.getcwd()+("/python")) #aggiungiamo il path di python, dove metteremo le librerie


model_number=3

#Parte 1: costruiamo il modello dal file di configurazione
from utilities import getModel #carichiamo la funzione model che usiamo per prendere i modelli  
fg,fe,fge,fgef=getModel("models/model_"+str(model_number)+".txt") #vedere getModel: restituisce funzione gaussiana, esponenziale e somma

#Nota: se abbiamo usato una notazione consistente
#dovremmo poter scegliere l'analisi variando solo il numero "3"
#che sta prima dell'estensione del file, qui e nei vari punti dove è necessario

#Parte 2: usiamo le utilities di root per il fit
fileHistos=ROOT.TFile("LLFile.root")#prendiamo il file creato prima
h3=fileHistos.Get("data_exercise_Likelihood_"+str(model_number)+"_txt")

#Parte 3: facciamo il likelihood scan
from utilities import txtToArray 

#otteniamo il vettore "unbinned": ho bisogno di riprendere il file di dati. Una copia è in "models"
x_array=txtToArray("models/exercise_Likelihood_"+str(model_number)+".txt")


#otteniamo il vettore "binned"
xbinned_array= np.array([ h3.GetBinContent(i) for i in range(1,h3.GetNbinsX()+1)])


#Esercizio:
#Usando le funzioni fge.Eval(x) e fge.Integral(xmin,xmax)
#proviamo a valutare la likelihood
#in funzione del numero di eventi di segnale e fondo

ntotal=len(x_array)
import math
nlls=[]

extended_nlls={}
#extended_nlls[(s,b)]
extended_nll=0

nll=0
lik=1.0
hnll=ROOT.TH1F("hnll_profile","negative log likelihood, profiled",ntotal,0,ntotal)
pois = ROOT.TF1("pois","TMath::Poisson(x,[0])")

def logpois(n,ni):
    #dobbiamo fare log(e^-ni ni^n/n!)
    #-ni + n*log(ni) -(nlog(n)-n)
    return (-ni+n*math.log(ni)-math.log(math.factorial(n)))#n*math.log(n)+n)
    #return (-ni+n*math.log(ni)-(n*math.log(n)-n))

lamb=fge.GetParameter(2)
mass=fge.GetParameter(0)
sigma=fge.GetParameter(1)
b=fge.GetParameter(4)

pois_nll_f = ROOT.TF1("pois_nll","TMath::Poisson(x,[0])")

hnll.Reset("ICES")
for s in range(0,ntotal+1):
    lik =0
    nll=0
    pois_nll=0

    bw=h3.GetBinWidth(1)

    fgef.FixParameter(3,s)#Fissiamo il numero di eventi nello scan
    fgef.FixParameter(5,ntotal)#Fissiamo il numero totale di eventi osservati 
    
    fgef.SetParameter(0,mass)
    fgef.SetParameter(2,lamb)
    fgef.SetParameter(1,sigma)
    fgef.SetParameter(4,(ntotal-s))
    
    h3min=h3.GetBinLowEdge(1)
    h3max=h3.GetBinLowEdge(1000)
    h3.Fit(fgef,"LEMSQ")
    b=fgef.GetParameter(4)
    #print("integrals ",fgef.Integral(h3min,h3max),h3.Integral())
    
    pois.SetParameter(0,s+b)
    #print("poisson parameter",s+b," value ", pois.Eval(ntotal))

    #Valutiamo la parte di di f(x) con i parametri ottenuti dal fit:
    fge.SetParameter(0,fgef.GetParameter(0))
    fge.SetParameter(1,fgef.GetParameter(1))
                     
    fge.SetParameter(2,fgef.GetParameter(2))

    fge.SetParameter(3,fgef.GetParameter(3)/(fgef.GetParameter(3)+fgef.GetParameter(4)))
    fge.SetParameter(4,fgef.GetParameter(4)/(fgef.GetParameter(3)+fgef.GetParameter(4)))
    
    doSkip=False
    #print("s ",s , "skipping?", doSkip)
    for x in x_array:
        lik=lik*fge.Eval(x)
        if(fge.Eval(x)>0):
            nll_xi=-2*math.log(fge.Eval(x))
        else:
            print(" likelihood is 0 for s",s," x ",x," skipping ")
            doSkip=True
            continue
        nll=nll + nll_xi
    if(doSkip):#if there is a problem in the evaluation of the likelihood, skip filling the event
        continue 
    #Valutiamo la parte di di f(x) con i parametri ottenuti dal fit:
    pois_nll_f.SetParameter(0,fgef.GetParameter(3)+fgef.GetParameter(4))
    #questo valore è molto piccolo --> usiamo la funzione "logaritmo della poissoniana" che abbiamo ricavato 
    nll=nll-2*logpois(ntotal,s+b)
    nlls.append(nll)
    hnll.SetBinContent(s,nll)
    
    
        
c1=ROOT.TCanvas()
hnll.Draw()
c1.Draw()
c1.SaveAs("nll_shape_profile.png")

fout=ROOT.TFile("zoomfile.root","UPDATE")
hnll.Write(hnll.GetName(),ROOT.TObject.kOverwrite)
fout.Close()

                              
                              
