import ROOT
import math

##################
# Helper functions
##################

# Check if a string can be a number
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def removeNegativeBins(h):
    for i in range(h.GetNbinsX()):
        if h.GetBinContent(i) < 0:
            h.SetBinContent(i, 0)

##################################
# To Fill Tag and Probe histograms
##################################

def makePassFailHistograms(sample, flag, bindef, var, sig_mass, bkg_mass):

    #####################
    # C++ Initializations
    #####################

    # For tree branches
    pair_mass = 0.
    el_IsoMVA94XV2 = 0.

    # For the loop
    nbins = 0
    nevts = 0
    frac_of_nevts = 0
    index = 0
    bnidx = 0
    outcount = 0
    weight = 0.0

    tree = ROOT.TChain(sample.tree)

    for p in sample.path:
        print ' adding rootfile: ', p
        tree.Add(p)

    if sample.puTree is not None:
        print ' - Adding weight tree: %s from file %s ' % (sample.weight.split('.')[0], sample.puTree)
        tree.AddFriend(sample.weight.split('.')[0], sample.puTree)
    #################################
    # Prepare hists, cuts and outfile
    #################################

    outfile = ROOT.TFile(sample.histFile, 'recreate')
    outfile = ROOT.TFile("results/UL2018_continuousSF_rightrange/tnpEleID/passingMVA94Xwp80isoV2/data_Run2018A_passingMVA94Xwp80isoV2_sweights.root", 'recreate')

    cutBinList = []

    hMVAsig_list = []
    hMVAbkg_list = []
    bin_formulas_list = ROOT.TList()

    for ib in range(len(bindef['bins'])):
        hMVAsig_list.append(ROOT.TH1D('%s_MVAsig' % bindef['bins'][ib]['name'], bindef['bins'][ib]['title'], 24, -12, 12))
        hMVAbkg_list.append(ROOT.TH1D('%s_MVAbkg' % bindef['bins'][ib]['name'], bindef['bins'][ib]['title'], 24, -12, 12))
        hMVAsig_list[ib].Sumw2()
        hMVAbkg_list[ib].Sumw2()

        cuts = bindef['bins'][ib]['cut']
        if sample.mcTruth:
            cuts = '%s && mcTrue==1' % cuts
        if sample.cut is not None:
            cuts = '%s && %s' % (cuts, sample.cut)

        if sample.isMC and sample.weight is not None:
            cutBin = '( %s ) * %s ' % (cuts, sample.weight)
            if sample.maxWeight < 999:
                cutBin = '( %s ) * (%s < %f ? %s : 1.0 )' % (cuts, sample.weight, sample.maxWeight, sample.weight)
        else:
            cutBin = '(%s)' % cuts
            #cutBin = 'tag_Ele_pt > 0'
	    temp = 0

        cutBinList.append(cutBin)

        bin_formulas_list.Add(ROOT.TTreeFormula('%s_Selection' % bindef['bins'][ib]['name'], cutBin, tree))
	print(('%s_Selection' % bindef['bins'][ib]['name'], cutBin, tree))
        nbins = nbins + 1

    	#tree.SetNotify(bin_formulas_list[ib])
    tree.SetNotify(bin_formulas_list)
      

    ######################################
    # Deactivate branches and set adresses
    ######################################

    # Find out which variables are used to activate the corresponding branches
    replace_patterns = ['&', '|', '-', 'cos(', 'sqrt(', 'fabs(', 'abs(', '(', ')', '>', '<', '=', '!', '*', '/', '[', ']']
    branches = " ".join(cutBinList) + " pair_mass " + " el_IsoMVA94XV2 "
    for p in replace_patterns:
        branches = branches.replace(p, ' ')

    branches = set([x for x in branches.split(" ") if x != '' and not is_number(x)])

    tree.SetBranchStatus("*", 0)

    for br in branches:
        tree.SetBranchStatus(br, 1)

    ################
    # Loop over Tree
    ################

    nevts = tree.GetEntries()
    frac_of_nevts = nevts // 20

    prob_sig = []
    prob_bkg = []

    print "Starting event loop to fill histograms.."

    for index in range(nevts):
        if index % frac_of_nevts == 0:
            print outcount, "%", sample.name
            outcount = outcount + 5

        tree.GetEntry(index)

        for bnidx in range(len(bindef['bins'])):
	    #if bnidx == 26:
	    if bnidx == 9:
            	weight = bin_formulas_list[bnidx].EvalInstance(0)
            	if weight:
    		    pdfsig_res = sig_mass.pdf(tree.pair_mass)
    		    pdfbkg_res = bkg_mass.pdf(tree.pair_mass)
		    prob_sig.append(pdfsig_res/(pdfsig_res + pdfbkg_res))
		    prob_bkg.append(pdfbkg_res/(pdfsig_res + pdfbkg_res))
            	    #hPair_list[bnidx].Fill(tree.pair_mass, weight)
            	    #hMVA_list[bnidx].Fill(tree.el_IsoMVA94XV2, weight)
            	    break

    import pandas as pd

    probs = pd.DataFrame(dict(sig=prob_sig, bck=prob_bkg))

    from hep_ml import splot
    sWeights = splot.compute_sweights(probs)

    counter = 0

    for index in range(nevts):
        if index % frac_of_nevts == 0:
            print outcount, "%", sample.name
            outcount = outcount + 5

        tree.GetEntry(index)

        for bnidx in range(len(bindef['bins'])):
	    #if bnidx == 26:
	    if bnidx == 9:
            	weight = bin_formulas_list[bnidx].EvalInstance(0)
            	if weight:
            	    #hPair_list[bnidx].Fill(pair_mass_leaf.GetValue(), weight)
            	    #hMVA_list[bnidx].Fill(el_IsoMVA94XV2_leaf.GetValue(), weight)
            	    hMVAbkg_list[bnidx].Fill(tree.el_IsoMVA94XV2, weight*sWeights.bck[counter])
            	    hMVAsig_list[bnidx].Fill(tree.el_IsoMVA94XV2, weight*sWeights.sig[counter])
		    counter = counter + 1
            	    break
    #####################
    # Deal with the Hists
    #####################

    #for ib in range(len(bindef['bins'])):
    removeNegativeBins(hMVAbkg_list[9])
    removeNegativeBins(hMVAsig_list[9])

    hMVAsig_list[9].Write(hMVAsig_list[9].GetName())
    hMVAbkg_list[9].Write(hMVAbkg_list[9].GetName())

    ##########
    # Clean up
    ##########

    tree.Delete()
    outfile.Close()

