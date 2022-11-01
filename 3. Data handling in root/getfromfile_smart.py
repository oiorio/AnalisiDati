import ROOT,sys
import numpy as np
import optparse

usage='python getfromfile_smart.py -i fileInput -o fileOutput -O RECREATE'
parser = optparse.OptionParser(usage)


parser.add_option('-i','--fileIn', dest='fileIn', type='string', default='data/exercise_Likelihood_1.txt', help='file di input')
parser.add_option('-o','--fileOut', dest='fileOut', type='string', default='LLFile1.root', help='file di output')
parser.add_option('-O','--fileOption', dest='fileOption', type='string', default='RECREATE', help='opzione di apertura del file')
parser.add_option('-v','--verbose', dest='verbose', action="store_true", default = False, help='modalità verbosa On')
(opt, args) = parser.parse_args()


#Definiamo una funzione per leggere un file di testo
from getfromfile_simple import txtToRoot

fileInName=opt.fileIn
fileOutName=opt.fileOut
fileOutOption=opt.fileOption
verbose=opt.verbose

#Modalità di default di lanciare un file in interattivo:
#Se caricato tramite import, il file non farà nulla
if __name__ =='__main__':
    #prendiamo le opzioni necessarie:

    
    hname=fileInName.replace("/","_").replace(".","_")

    outFile=txtToRoot(fileInName,fileOutName,fileOutOption=fileOutOption,hname=hname,verbose=verbose)

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

        
