import ROOT,sys
import numpy as np



#Prendiamo un file con il nome del path
fIn=open("data/exercise_Likelihood_1.txt","r")
xs=(fIn.read().split("\n"))#leggiamolo col metodo read, dividendo le righe

#creiamo un istogramma:
nbins=100
xmin=0
xmax=2000
hname="hx"

histo=ROOT.TH1F(hname,"x",nbins,xmin,xmax)

#facciamo un loop sulle righe:
for x in xs:
    x=x.replace("'","").replace(" ","")#eliminiamo le virgolette e gli spazi vuoti
    print("x is ",x)
    if(x==''):
        continue
    fx=float(x)
    #x_array= np.append(x_array,[x])
    #print(lx)
    histo.Fill(fx)

print(histo.GetEntries())    

c1=ROOT.TCanvas()    
c1.Draw()
histo.Draw()    
c1.SaveAs("example.png")
