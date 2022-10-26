import ROOT

c1= ROOT.TCanvas("c1") #Definisco la canvas su cui disegnare

h1d = ROOT.TH1F ("nome","titolo",100,0,100)
h1d.Fill(10.1)
h1d.Scale(1.30)
h1d.Draw()
c1.SaveAs("myexamplehisto.png")


mypoly = ROOT.TF1("polynomial","[0]+x*[1]",0,1000)
mypoly.SetParameters(10,-0.008)
mypoly.Draw()

c1.SaveAs("mypoly.png")

h2d = ROOT.TH1D("h2name","h2 extracted from poly",100,0,100)
h2d.FillRandom("polynomial",5000)
h2d.Scale(0.01)
h2d.Draw()
c1.SaveAs("genhisto2.png")

h1d.Add(h2d)
h1d.Draw()
c1.SaveAs("sumhisto2.png")
