import ROOT
import numpy as np

def getModel(fileName="models/model_1.txt",modelName='',fRange=(0,2000)):
    gauss="1/([1]*sqrt(2*TMath::Pi()))*exp( ( (x-[0] )*(x-[0]) )/(2*[1]*[1] ) )"
    expo="1/[0]*exp(-x/[0])"
    gaussexpo="[4]/[2]*exp(-x/[2]) + [3]/([1]*sqrt(2*TMath::Pi()))*exp( -( (x-[0] )*(x-[0]) )/(2*[1]*[1] ) )"
    gaussexpofrac="([4]/([3]+[4])/[2]*exp(-x/[2]) + [3]/([3]+[4])/([1]*sqrt(2*TMath::Pi()))*exp( -( (x-[0] )*(x-[0]) )/(2*[1]*[1] ) ) )"
    gaussexpofrac="TMath::Power(TMath::Poisson([5],[4]+[3]),1/[5] )*([4]/([3]+[4])/[2]*exp(-x/[2]) + [3]/([3]+[4])/([1]*sqrt(2*TMath::Pi()))*exp( -( (x-[0] )*(x-[0]) )/(2*[1]*[1] ) ) )"

    mass=0
    sigma=0
    lam=0
    
    fIn = open(fileName)
    flines= fIn.readlines()

    parameters={}
    for l in flines:
        ls=l.split()
        if(len(ls)==2):
            parameters[ls[0]]=float(ls[1])
            
    
    if modelName=='':
        modelName=fileName.replace("/","_").replace(".txt",".").replace(".","")

    if("mass" in parameters.keys() and "sigma" in parameters.keys() ):
        mass=parameters["mass"]
        print("mass",mass)
        sigma=parameters["sigma"]
        print("sigma",sigma)


    fgauss= ROOT.TF1(modelName+"g",gauss,fRange[0],fRange[1])
    fgauss.SetParameter(0,mass)
    fgauss.SetParameter(1,sigma)

    if("lambda" in parameters.keys()):
        lam=parameters["lambda"]        

    fexpo= ROOT.TF1(modelName+"e",expo,fRange[0],fRange[1])
    fexpo.SetParameter(0,lam)

    fgaussexpo= ROOT.TF1(modelName+"ge",gaussexpo,fRange[0],fRange[1])
    fgaussexpo.SetParameter(0,mass)
    fgaussexpo.SetParameter(1,sigma)
    fgaussexpo.SetParameter(2,lam)
    fgaussexpo.SetParameter(3,100)
    fgaussexpo.SetParameter(4,100)

    fgaussexpofrac= ROOT.TF1(modelName+"gef",gaussexpofrac,fRange[0],fRange[1])
    fgaussexpofrac.SetParameter(0,mass)
    fgaussexpofrac.SetParameter(1,sigma)
    fgaussexpofrac.SetParameter(2,lam)
    fgaussexpofrac.SetParameter(3,100)
    fgaussexpofrac.SetParameter(4,100)

    
    return fgauss,fexpo,fgaussexpo,fgaussexpofrac


def txtToArray(fileInName,verbose=False):
    fIn=open(fileInName)
    x_array=np.array([])
    for l in fIn.readlines():
        lx=l.split()
        if(verbose):
            print(lx)
        if(len(lx)):
            x=float(lx[0])
            x_array= np.append(x_array,[x])

    return x_array
