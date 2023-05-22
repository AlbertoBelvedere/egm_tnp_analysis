#include <iostream>
#include <math.h>
#include <TTree.h>
#include <TFile.h>
#include <TH1F.h>
#include <TProfile.h>
#include <TH2F.h>
#include <TStyle.h>
#include <TCanvas.h>


void doRF(TString infilename, TString outfilename, int lowbin){

	TFile *ntuple;
	ntuple = TFile::Open("/eos/cms/store/group/phys_egamma/tnpTuples/tomc/2020-05-20/UL2018/merged/"+infilename);
	
	TTree *tree;
	ntuple->GetObject("tnpEleIDs/fitter_tree", tree);
	
	Float_t el_IsoMVA94XV2;
	Float_t tag_Ele_pt;
	Float_t tag_sc_eta;
	Float_t el_q;
	Float_t tag_Ele_q;
	Float_t tag_Ele_trigMVA;
	Float_t el_sc_eta;
	Float_t el_pt;
	
	TBranch	*b_el_IsoMVA94XV2; 
	TBranch	*b_tag_Ele_pt; 
	TBranch	*b_tag_sc_eta; 
	TBranch	*b_el_q; 
	TBranch	*b_tag_Ele_q; 
	TBranch	*b_tag_Ele_trigMVA; 
	TBranch	*b_el_sc_eta; 
	TBranch	*b_el_pt; 

	tree->SetBranchAddress("el_IsoMVA94XV2", &el_IsoMVA94XV2, &b_el_IsoMVA94XV2);
	tree->SetBranchAddress("tag_Ele_pt", &tag_Ele_pt, &b_tag_Ele_pt);
	tree->SetBranchAddress("tag_sc_eta", &tag_sc_eta, &b_tag_sc_eta);
	tree->SetBranchAddress("el_q", &el_q, &b_el_q);
	tree->SetBranchAddress("tag_Ele_q", &tag_Ele_q, &b_tag_Ele_q);
	tree->SetBranchAddress("tag_Ele_trigMVA", &tag_Ele_trigMVA, &b_tag_Ele_trigMVA);
	tree->SetBranchAddress("el_sc_eta", &el_sc_eta, &b_el_sc_eta);
	tree->SetBranchAddress("el_pt", &el_pt, &b_el_pt);

	TH1::SetDefaultSumw2();
	int nbin;

	TH1F* h_IsoMVA94XV2;

	if(lowbin == -10) nbin = 100;
	else nbin = 20;

	h_IsoMVA94XV2 = new TH1F("IsoMVA94XV2", "", nbin, lowbin, 1);

	Long64_t nentries = tree->GetEntriesFast();
	for(int jEntry = 0; jEntry < nentries; ++jEntry){
		tree->GetEntry(jEntry);
		//TnP cuts 
		if (el_pt < 10) continue; 
		if (el_pt < 20 && tag_Ele_trigMVA < 0.92) continue; 	//trigMVA
		if (fabs(el_sc_eta) > 2.5) continue; 			//probe_eta
		if (tag_Ele_pt < 35) continue; 				//tag_pt
		if (fabs(tag_sc_eta) > 2.17) continue; 			//tag_eta
		if (el_q*tag_Ele_q > 0) continue;			//charge
		if (lowbin == -1){
			if (el_IsoMVA94XV2 < -1) continue;
		};

		//Filling histogram
		h_IsoMVA94XV2->Fill(el_IsoMVA94XV2);
	}

	gStyle->SetOptStat(0000);

	TFile* outfile;

	outfile = new TFile("histofiles/"+outfilename, "RECREATE");
	outfile->cd();
	h_IsoMVA94XV2->Write("h_IsoMVA94XV2");
	outfile->Write();
	outfile->Close();
	
	ntuple->Close();
}
