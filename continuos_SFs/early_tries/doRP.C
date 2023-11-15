#include "stdio.h"
#include "TH1.h"
#include "TH2.h"
#include "UnfPlottingTools.h"
//#include "constants.h"

void doRP()
{
	int n_file = 2;
	int nplots = 2;
	double factor = 1.0;
	TString plots[2] = {"h_IsoMVA94XV2", "h_pair_mass"};
	vector<TH1*> histos;
	TCanvas *c[2] = {0};
	TCanvas *c2[2] = {0};
	
	TFile *f[2] = {0};
	f[0] = TFile::Open("histofiles/Data.root");
	f[1] = TFile::Open("histofiles/MC.root");
	
	for(int i =0; i < nplots; i++){
		for(int j = 0; j < n_file; j++){
			histos.push_back((TH1*)f[j]->Get(plots[i]));
			histos[j]->Scale(factor/histos[j]->Integral("width"));
		}
		c[i] = UnfPlottingTools::th1_ratio_plot(histos, 0, 0, 0.5, 1.5, 1, "Data/MC");
		c[i]->Print("plots/"+plots[i]+"_ratio.pdf", ".pdf");
		histos.clear();
	}
	for(int i =0; i < nplots; i++){
		c2[i] = UnfPlottingTools::PlotTH1((TH1*)f[0]->Get(plots[i]), 0, 0, 0, "Data/MC");
		c2[i]->Print("plots/"+plots[i]+"_data.pdf", ".pdf");
	}
}

