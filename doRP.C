#include "stdio.h"
#include "TH1.h"
#include "TH2.h"
#include "UnfPlottingTools.h"
//#include "constants.h"

void doRP(TString outputfile, int is_reduced)
{
    int n_file = 2;
    double factor = 1.0;
    vector<TH1*> histos;
    TCanvas *c;

    TFile *f[2] = {0};
    if (is_reduced == 1){
    	f[0] = TFile::Open("histofiles/Data_reduced_0.root");
    	f[1] = TFile::Open("histofiles/MC_reduced_0.root");
    }
    else{
    	f[0] = TFile::Open("histofiles/Data.root");
    	f[1] = TFile::Open("histofiles/MC.root");
    }
 
    for(int j = 0; j < n_file; j++){
       	histos.push_back((TH1*)f[j]->Get("h_IsoMVA94XV2"));
        histos[j]->Scale(factor/histos[j]->Integral("width"));
    }
    c = UnfPlottingTools::th1_ratio_plot(histos, 0, 0, 0.5, 1.5, 1, "Data/MC");
    c->Print(outputfile, ".pdf");
    histos.clear();
}

