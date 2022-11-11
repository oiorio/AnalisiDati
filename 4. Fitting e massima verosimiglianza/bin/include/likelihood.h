#include "TFile.h"
#include "TTree.h"
#include "TH1.h"
#include "TFitResult.h"
#include "TF1.h"
#include "TH2.h"
#include "TCanvas.h"
#include <iostream>
#include <TROOT.h>
#include "TRint.h"
#include <sstream>
#include "TMath.h"
#include <fstream>
#include <TStyle.h>

using namespace std;
float nlleval(TF1* f1, vector<float >xs){
  float nll=0;

  for (int i = 0;i <xs.size();++i){
    //for (int i = 0;i <5;++i){
    float xi = xs.at(i);
    float value=f1->Eval(xi);
    nll-=value;
  }
  return nll;
}

//void macro_likelihoodscan(string filename="exercise_Likelihood_1.txt",string model_name="model_1.txt"){
void likelihoodscan(int n_analysis=1, string folder= "./macros/", string mode="2D,profile"){
  string n_an=to_string(n_analysis);
  string filename = folder+"/exercise_Likelihood_"+n_an+".txt";
  string model_name= folder+"/model_"+n_an+".txt";
  ifstream f(filename);
  ifstream mod(model_name);
  float xs;
  float minx=0., maxx=1000;
  TH1F * h1= new TH1F("h1","h1",1000,minx,maxx);
  vector<float> values;

  TCanvas c1("c1");
  
  while(!f.eof()){
    f >> xs;
    h1->Fill(xs);
    values.push_back(xs);
      
  };
  
    float mass=0,sigma=0,lambda=0;
  string tmp="";
  mod>>tmp>>mass;
  mod>>tmp>>sigma;
  mod>>tmp>>lambda;
  cout << mass << sigma <<lambda<<endl;
  h1->Draw();
  c1.SaveAs(("Data"+n_an+".png").c_str());
  c1.SaveAs(("Data"+n_an+".pdf").c_str());

  string pois_formula ="TMath::Power(TMath::Poisson([0],[1]+[2]),1./[0])";
  string gauss_formula = "(1./([4]*sqrt(2*TMath::Pi()))*TMath::Exp(((-(x-[3])**2)/(2*[4]*[4])) ) )";
  string exp_formula = "(TMath::Exp((-x/[5]))/[5])";
  string pois_sb_formula=  "1*"+pois_formula+"*([1]/([1]+[2])*"+gauss_formula+" + [2]/([1]+[2])*"+exp_formula+")";

  //Logarithms to evaluate the sum:
  string log_pois_formula ="log(TMath::Poisson(x,[1]+[2]))";
  string log_sb_formula=  "log([1]/([1]+[2])*"+gauss_formula+" + [2]/([1]+[2])*"+exp_formula+")";

  TF1 *lpf = new TF1("log_pois",log_pois_formula.c_str(),0,4000);
  TF1 *lsbf= new TF1("log_sb",("[0]*"+log_sb_formula).c_str(),minx,maxx);

  //  cout<<" the formula is"<< pois_sb_formula <<endl;
  
  
  
  float s = 240;
  float b = values.size()-s;
  float N= values.size();
  int step=20;

  if(mode.find("2D")!=string::npos){
      // 2d likelihood scan  part
      //  string pois_formula ="TMath::Poisson([0],[0])";
    
      cout << "I want to scan it over s and b, let's take the logarithm:"<<endl;
      cout <<" log formula: \n "<<  log_sb_formula<<endl;

      
      TH2D *hnll= new TH2D("hnll","negative log likelihood scan",int(N/step),0,N,int(N/step),0,N);

      vector<double> nll_scan;
      vector<pair<int,int> > sb_scan;
      for (int bi=N;bi>0;bi=bi-step){
    
	float completion= (1-float(bi)/N) *100.0;
	for (int si=0;si<N;si=si+step){
	  
	  lpf->SetParameters(N,si,bi);
	  lsbf->SetParameters(1.,si,bi,mass,sigma,lambda);
	  
	  float poisnll=-1*lpf->Eval(N);
	  float nll = poisnll;
	  nll = nll+nlleval(lsbf,values);
	  
	  
	  nll_scan.push_back(nll);
	  sb_scan.push_back(pair<int,int>(bi,si));
	  
	  int bin_b=bi,bin_s=si;
	  bin_b=int(bi/step);
	  bin_s=int(si/step);
	  hnll->SetBinContent(bin_b,bin_s,nll);
	  
	}
	cout<<" Advancement:"<< setprecision(2) <<completion<<"\%; b=" <<  bi <<endl;
      }
      int minnll_idx=min_element(nll_scan.begin(),nll_scan.end())-nll_scan.begin();
      cout << " min nll "<< nll_scan.at(minnll_idx)<< " at s,b "<<sb_scan.at(minnll_idx).second<< " "<<sb_scan.at(minnll_idx).first<<endl; 
      gStyle->SetOptStat(0000);
      hnll->Draw("colZ");
      c1.SaveAs(("Nll"+n_an+".png").c_str());
      c1.SaveAs(("Nll"+n_an+".pdf").c_str());
  }   
  
  if(mode.find("profile")!=string::npos){
    cout << " Let's do the fit to data! "<<endl;

    TF1* ll=new TF1("ll",pois_sb_formula.c_str(),minx,maxx);
    ll->SetParameters(values.size(),200,1200,mass,sigma,lambda);
    ll->FixParameter(0,values.size());
    TFitResultPtr fitres =  h1->Fit("ll","LEMS");
    fitres->Print("V");
    ll->Draw("same");
    cout << "Nota Bene: this is a binned fit!"<<endl;
    
    
    lpf->SetParameters(N,ll->GetParameter(1),ll->GetParameter(2));
    lsbf->SetParameters(1,ll->GetParameter(1),ll->GetParameter(2),ll->GetParameter(3),ll->GetParameter(4),ll->GetParameter(5));
    double min2nll=-2*lpf->Eval(N)+2*nlleval(lsbf,values);
    
    vector<double>  nllscan;
    int steps_pnll=1;
    TH1D * prof_nllscan= new TH1D("profnll","-2 log profile likelihood ratio scan",N/steps_pnll,0,N);
    for (int i =0;i< N/steps_pnll;i++){
      float si=steps_pnll*i;
      //cout << " step n "<< i <<" si is "<<si<<endl;
      ll->SetParameters(values.size(),si,1200,mass,sigma,lambda);
      ll->FixParameter(1,si);
      
      h1->Fit("ll","LEMSQ");
      
      lpf->SetParameters(N,ll->GetParameter(1),ll->GetParameter(2));
      lsbf->SetParameters(1,ll->GetParameter(1),ll->GetParameter(2),ll->GetParameter(3),ll->GetParameter(4),ll->GetParameter(5));
      double nllratio=-2*lpf->Eval(N)+2*nlleval(lsbf,values)-min2nll;
      
      nllscan.push_back(nllratio);
      prof_nllscan->SetBinContent(i,nllratio);
    }
    
    prof_nllscan->Draw("l");
    c1.SaveAs(("ProfNllScan"+n_an+".png").c_str());
    c1.SaveAs(("ProfNllScan"+n_an+".pdf").c_str());
  }
}

