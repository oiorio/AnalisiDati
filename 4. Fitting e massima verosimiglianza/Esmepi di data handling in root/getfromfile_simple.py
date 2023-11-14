import ROOT,sys
import numpy as np


fileInName="data/exercise_Likelihood_1.txt"
fileOutName="LLFile.root"

#Definiamo una funzione per leggere un file di testo
def txtToRoot(fileInName,fileOutName,hname="hx",nbins=100,fileOutOption="RECREATE",dryrun=False,verbose=False):
    fIn=open(fileInName)
    x_array=np.array([])
    for l in fIn.readlines():
        lx=l.split()
        if(verbose):
            print(lx)
        if(len(lx)):
            x=float(lx[0])
            x_array= np.append(x_array,[x])
            
    xmin=np.min(x_array)
    xmax=np.max(x_array)
    histo=ROOT.TH1F(hname,"x",nbins,xmin,xmax)

    for x in x_array:histo.Fill(x)
    
    fOut=ROOT.TFile(fileOutName,fileOutOption)
    histo.Write()
    fOut.Close()
    return fOut
    
#Modalità di default di lanciare un file in interattivo:
#Se caricato tramite import, il file non farà nulla
if __name__ =='__main__':
    args=sys.argv
    #il vettore "args" ha sempre come argomento 0 il nome del file che si sta girando
    print("l'argomento 0 è:",args[0])
    if len(args)>1:
        #il primo argomento che passiamo è il file di input
        fileInName=str(args[1])
    if len(args)>2:
        #il secondo argomento è il file di output
        fileOutName=str(args[2])
    #nota bene: quando ci sono molti argomenti questa cosa diventa complicata! C'è una soluzione...
    outFile=txtToRoot(fileInName,fileOutName,verbose=False)

    #apriamo il file :
    print("output file is:",outFile,"Is Open?",outFile.IsOpen())
    #non è aperto, perché lo abbiamo passato come target da "closed!"
    #tipicamente si fa così:

    outFile=ROOT.TFile.Open(outFile.GetName())
    print("Is Open now?",outFile.IsOpen())
    #Ora stampiamo la lista di chiavi:
    print( outFile.GetListOfKeys().Print())
    for k in outFile.GetListOfKeys():
        print ("key: ",k.GetName())
        h= outFile.Get(k.GetName())
        print ("histo: ",h.GetName(),", entries :",h.GetEntries())

        
