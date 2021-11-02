void macro_example(){
  TCanvas c1("c1");
  TH1D * h1d = new TH1D ("h1d","h1d title",100,0,100); //Nota: affinchè gli istogrammi persistano è necessario fare puntatori #rootthings
  h1d->Fill(10.1);
  h1d->Scale(1.3);
  TH1D * h2d = new TH1D("h2d","h2d extracted from poly",100,0,100);
  TF1 * mypoly = new TF1("polynomial","[0]+x*[1]",0,100);
  mypoly->SetParameters(10,-0.008);
  h2d->FillRandom("polynomial",5000);
  h2d->Scale(0.01);
  h1d->Add(h2d);

  h1d->Draw();
  c1.SaveAs("Sum_Example.png");
}
