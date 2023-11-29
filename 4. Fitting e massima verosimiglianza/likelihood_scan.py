import ROOT
import sys,os, math
import numpy as np
sys.path.append(os.getcwd()+("/python")) #aggiungiamo il path di python, dove metteremo le librerie
print(sys.path)


#Parte 1: costruiamo il modello dal file di configurazione
from utilities import getModel #carichiamo la funzione model che usiamo per prendere i modelli  
fg,fe,fge,fgefrac=getModel("models/model_3.txt") #vedere getModel: restituisce funzione gaussiana, esponenziale e somma

#Nota:ls  se abbiamo usato una notazione consistente
#dovremmo poter scegliere l'analisi variando solo il numero "3"
#che sta prima dell'estensione del fls ile, qui e nei vari punti dove è necessario

#Parte 2: usiamo le utilities di root per il fit
print(fge)
fileHistos=ROOT.TFile("LLFile.root")#prendiamo il file creato prima

h3=fileHistos.Get("data_exercise_Likelihood_3_txt")
h3.Fit(fge.GetName(),"I")

c1=ROOT.TCanvas()
c1.Draw()
h3.Draw()
c1.SaveAs("fitGaussExpo1.png")

#Parte 3: facciamo il likelihood scan
from utilities import txtToArray #carichiamo la funzione model che usiamo per prendere i modelli  

#otteniamo il vettore "unbinned": ho bisogno di riprendere il file di dati. Una copia è in "models"
x_array=txtToArray("models/exercise_Likelihood_3.txt")
print (x_array)

#otteniamo il vettore "binned"
xbinned_array= np.array([ h3.GetBinContent(i) for i in range(1,h3.GetNbinsX()+1)]) 
#print (xbinned_array)

#Esercizio:
#Usando le funzioni fge.Eval(x) e fge.Integral(xmin,xmax)
#proviamo a valutare la likelihood
#in funzione del numero di eventi di segnale e fondo

#primo loop che dobbiamo fare è su s:

n_eventi = len(x_array)
nll_vector=[]
nll_values = ROOT.TH1F("nll_values","nll_values",n_eventi,0,n_eventi)

for s in range(0,n_eventi):
    #per ognuno di questi valori del parametro
    #valutiamo la funzione di verosimiglianza
    #caso "semplificato": n_eventi= s+b ==> b=n_eventi - s
    b = n_eventi - s
    #prima di valutare la funzione dobbiamo settare i parametri a quelli che
    #servono per il likelihood scan!
    #Quindi i parametri mean, sigma e lambda li mettiamo ai valori noti
    #il parametro s (e di conseguenza il parametro b) cambiano lungo il nostro scan
    fgefrac.SetParameters(800,50,200,s,b)
    nll = 0
    likelihood_value=1
    #print (" signal hypothesis is s = " +str(s))
    for xi in x_array:
        value_xi = fgefrac.Eval(xi)
        likelihood_value= likelihood_value*value_xi
        nll = nll -2 * math.log(value_xi)
        #print(" likelihood value is: ", likelihood_value , " nll is ", nll)
    #print( " the negarive log likelihood of the sample for the above value of s is: ",nll)
    nll_values.SetBinContent(s+1,nll)
    nll_vector.append(nll)


nll_values.Draw("")
c1.SaveAs("nll_values_1D_no_poisson.png")
out_content = ROOT.TFile.Open("likelihood_exercise.root","RECREATE")
nll_values.Write()

#aggiungiamo ora un pezzo poissoniano per il numero di eventi e la varazione del parametro b
#dobbiamo scrivere la poissoniana intorno ad s+b e aggiungere il contributo corrispondente nella nostra
#extended maximum likelihood

#ora dobbiamo considerare due loop: sul parametro s e sul parametro b
pois=ROOT.TF1("Nevents","TMath::Poisson(x,[0])",0,n_eventi)

nsplit=5.0

nll_values_2D_counting = ROOT.TH2F("nll_values_2D_counting","nll_values_2D_counting",n_eventi,0,n_eventi, n_eventi, 0, n_eventi)
nll_values_2D_shape = ROOT.TH2F("nll_values_2D_shape","nll_values_2D_shape",int(n_eventi/nsplit),0,n_eventi, int(n_eventi/nsplit), 0, n_eventi)
for s in range(0,n_eventi,int(nsplit)):
    for b in range(0,n_eventi,int(nsplit)):
        #i valori per cui s+b è molto lontano da n_eventi saranno soppressi dal termine di probabilità
        #poissoniana della likelihood! Scriviamo infatti:
        pois.SetParameter(0,s+b)
        #scordiamoci della shape e facciamo solo un counting experiment:
        #cosa succederà? --> il valore migliore sarà proprio s+b = n_eventi, il numero di eventi nei dati!
        print("s and b are: "+str(s)+" , "+str(b), " the likelihood is: ", pois.Eval(n_eventi))
        nll_poisson=0
        if(pois.Eval(n_eventi)!=0):
            nll_poisson=-2*math.log(pois.Eval(n_eventi))
            nll_values_2D_counting.SetBinContent(int((s+1)/nsplit),int((b+1)/nsplit),-2*math.log(pois.Eval(n_eventi)))
        else:
            nll_poisson=0
            nll_values_2D_counting.SetBinContent(s+1,b+1,0)

        #se vogliamo considerare l'extended nll dobbiamo usare anche la funzione:
        fgefrac.SetParameters(800,50,200,s,b)

        nll = 0
        likelihood_value=1
        for xi in x_array:
            value_xi = fgefrac.Eval(xi)
            likelihood_value= likelihood_value*value_xi
            nll = nll -2 * math.log(value_xi)

        if(nll_poisson!=0):
            nll_tot= nll+nll_poisson
            nll_values_2D_shape.SetBinContent(int((s+1)/nsplit),int((b+1)/nsplit),nll_tot)
            print("nlltot is ", nll_tot)
        else:
            nll_values_2D_shape.SetBinContent(s+1,b+1,0)

nll_values_2D_counting.Draw("colZ")
c1.SaveAs("nll_2D_counting.png")
nll_values_2D_shape.Draw("colZ")
c1.SaveAs("nll_2D_shape.png")
nll_values_2D_counting.Write()
nll_values_2D_shape.Write()

#parte binnata, i dati sono xbinned_array

nsplit=10.0 

pois_bin = ROOT.TF1("TMath::Poisson(x,[0])",0,nevents)

nll_values_2D_shape_binned = ROOT.TH2F("nll_values_2D_shape_binned","nll_values_2D_shape_binned",int(n_eventi/nsplit),0,n_eventi, int(n_eventi/nsplit), 0, n_eventi)

for s in range(0,n_eventi,int(nsplit)):
    for b in range(0,n_eventi,int(nsplit)):
        #per valutare la likelihood binned come possiamo fare?

        #se vogliamo considerare l'extended nll dobbiamo usare anche la funzione:
        fgefrac.SetParameters(800,50,200,s,b)

        nll=0
        for i in range(len(xbinned_array)): 
        #questo fa le veci del loop sugli eventi:
        #for xi in x_array:
        #    value_xi = fgefrac.Eval(xi)
            x_data= xbinned[i]
            x_i_min= h3.GetBinLowEdge(i)
            x_i_max= h3.GetBinLowEdge(i+1)
            epsilon_i=fgefrac.Integral(x_i_min, x_i_max)
            nu_i=(s+b)*epsilon_i
            pois_bin.SetParamter(0,nu_i)  # qui ci vuole epsilon_i * s+b#)
            pois_i = pois_bin.Eval(x_data)
            nll_i = 0
            if pois_i != 0:
                nll_i = -2*math.log(pois_i)
            else :
                nll_i = 10000
            if(s==80 and b ==770):
                print(" bin is ",i, " xmin ", x_i_min, " xmax ", x_i_max, " nu is ", nu_i, " epsilon ", epsilon_i, )
            nll= nll+nll_i
        nll_values_2D_shape_binned.SetBinContent(int((s+1)/nsplit),int((b+1)/nsplit),nll)            

nll_values_2D_shape_binned.Draw()
c1.SaveAs("nll_values_2D_shape_binned.png")
nll_values_2D_shape_binned.Write()
out_content.Close()
    #break

