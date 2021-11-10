#include "TFile.h"
#include "TTree.h"
#include "TH1.h"
#include "TF1.h"
#include "TH2.h"
#include "TCanvas.h"
#include <iostream>
#include <TROOT.h>
#include "TRint.h"
#include "../include/likelihood.h"
#include <sstream>

int main(int argc,char **argv){
  
  //metto due argomenti: una stringa , preso da argv[1] e un numero, preso da argv[2]
  int analysis=0;
  string folder="./macros/";
  string mode = "2Dprofile";

    analysis= stof(string(argv[1]));

  if (argc>2)folder= (string(argv[2]));
  if (argc>3)mode= (string(argv[3]));


  likelihoodscan(analysis,folder,mode);

  
    
}

  //  getTree("Data_new.root","outputhistosdBl0p0075.root");
  //  scancuts("outputhistosdBl0p0075.root");
  
  //CompareChannels("TT.root","DYJets_MC","Data_new.root","comparison.root");

