import ROOT
import sys,os
import numpy as np
sys.path.append(os.getcwd()+("/python")) #aggiungiamo il path di python, dove metteremo le librerie
print(sys.path)


#Parte 1: costruiamo il modello dal file di configurazione
from utilities import getModel #carichiamo la funzione model che usiamo per prendere i modelli  
fg,fe,fge,fgef=getModel("models/model_3.txt") #vedere getModel: restituisce funzione gaussiana, esponenziale e somma

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
nlls=[]

extended_nlls={}
extended_binned_nlls={}
#extended_nlls[(s,b)]
extended_nll=0

nll=0
lik=1.0
hnll=ROOT.TH1F("hnll","hnll",ntotal,0,ntotal) 
hext_nll=ROOT.TH2F("hext_nll","hext_nll",int(ntotal/5.),0,ntotal,int(ntotal/5.),0,ntotal) 
hext_binned_nll=ROOT.TH2F("hext_binned_nll","hext_binned_nll",int(ntotal/5.),0,ntotal,int(ntotal/5.),0,ntotal) 

pois = ROOT.TF1("pois","TMath::Poisson(x,[0])")
pois_bin = ROOT.TF1("pois_bin","TMath::Poisson(x,[0])")


pois_nll = 0
binned_nll = 0 
#gaussexpo2 = ROOT.TF1("fge2","[0]*gaus+[1]*expo",0,1000)
#facciamo ora il caso 1d (non extended). In questo caso scegliamo s vincolato a b:
for s in range(0,ntotal):
    nll=0
    fge.SetParameter(3,s/ntotal)
    fge.SetParameter(4,(ntotal-s)/ntotal)
    for x in x_array:
        lik=lik*fge.Eval(x)
        nll_xi=-2*math.log(fge.Eval(x))
        nll=nll + nll_xi
    nlls.append(nll)
    hnll.SetBinContent(s,nll)
    smin=np.min(np.array(nlls))

def logpois(n,ni):
    #dobbiamo fare log(e^-ni ni^n/n!)
    #-ni + n*log(ni) -(nlog(n)-n)
    return (-ni+n*math.log(ni)-math.log(math.factorial(n)))#n*math.log(n)+n)

    
#facciamo ora il caso 2d: non vincoliamo s a b e
#consideriamo la somma fluttuare poissonianamente
for s in range(0,ntotal,5):
    for b in range (1,ntotal,5):
        nll=0
        pois_nll=0
        binned_nll=0

        #if(abs(s+b-ntotal)>30 ):continue
        fge.SetParameter(3,s/(s+b))
        fge.SetParameter(4,b/(s+b))
        pois.SetParameter(0,s+b)
        
        nllpois_stir=logpois(ntotal,s+b)
        #print("poisson parameter",s+b," value ",pois.Eval(ntotal), " log pois stirling ",nllpois_stir )
                
        for x in x_array:
            lik=lik*fge.Eval(x)
            nll_xi=-2*math.log(fge.Eval(x))
            nll=nll + nll_xi
        
        nll=nll-2*nllpois_stir
        extended_nlls[(s,b)]=nll
        hext_nll.SetBinContent(int(s/5),int(b/5),nll)

        for i_bin in range(len(xbinned_array)):
            fge.SetParameter(3,s/(s+b))
            fge.SetParameter(4,b/(s+b))
            
            x3data=h3.GetBinContent(i_bin+1)#il conteggio dei bin nei TH1 va da 1 a nbins+1
            x3prediction=(s+b)*fge.Integral(h3.GetBinLowEdge(i_bin+1),h3.GetBinLowEdge(i_bin+2))#così prendiamo gli estremi di integrazione
            #print("bin # ", i_bin+1, " data ",x3data, " prediction ", x3prediction)
            pois_bin.SetParameter(0,x3prediction)
            nll_xi=-2*math.log(pois_bin.Eval(x3data))
            nll_xi=-2*logpois(x3data,x3prediction)
            binned_nll=binned_nll+nll_xi
            #print("s,b ",s,b, "nll_xi ", nll_xi," binned nll ",binned_nll)
        print("s,b ",s,b, " binned nll ",binned_nll)
        extended_binned_nlls[(s,b)]=binned_nll
        hext_binned_nll.SetBinContent(int(s/5),int(b/5),binned_nll)
            
hnll.Draw()
c1.Draw()
c1.SaveAs("nll_shape.png")

fout=ROOT.TFile("zoomfile.root","RECREATE")
hnll.Write()
hext_nll.Write()
hext_binned_nll.Write()
fout.Close()

hext_nll.Draw("Colz")
c1.Draw()
c1.SaveAs("nll_2d_shape.png")

hext_binned_nll.Draw("Colz")
c1.Draw()
c1.SaveAs("binned_nll_2d_shape.png")

                              
