import ROOT
import os


# Plotting of all years to be implemented

def makeCanvas(sample, tnpBins, plotDir):
    # Stack histos belonging to same group
    ROOT.gStyle.SetOptStat(0)
    ROOT.gROOT.SetBatch(ROOT.kTRUE)

    dataSample = ROOT.TFile(sample.hMVA_data, "read")
    mcSample = ROOT.TFile(sample.hMVA_mc, "read")
    ratioSample = ROOT.TFile(sample.hMVA_ratio, "read")

    variables = ['MVA', 'Pair']

    path_pair = os.path.join(plotDir, "Pair_ratio")
    path_MVA = os.path.join(plotDir, "MVA_ratio")

    if not os.path.exists( path_pair ):
       os.makedirs(path_pair)
    
    if not os.path.exists( path_MVA ):
       os.makedirs(path_MVA)

    for i in variables: 
        for ib in range(len(tnpBins['bins'])):
            h_data = dataSample.Get('%s_%s' % (tnpBins['bins'][ib]['name'], i)) 
            h_mc = mcSample.Get('%s_%s' % (tnpBins['bins'][ib]['name'], i)) 

            h_data.Scale(1.0 / h_data.Integral())
            h_mc.Scale(1.0 / h_mc.Integral())
	    

	    h_mc_no_errors = h_mc.Clone()
            for ibin in range(h_mc_no_errors.GetNbinsX()+2):
                    h_mc_no_errors.SetBinError(ibin, 0)

            mc_error_contribution = h_mc.Clone()
            for ibin in range(mc_error_contribution.GetNbinsX()+2):
                if mc_error_contribution.GetBinContent(ibin) != 0:
                    rel_unc = mc_error_contribution.GetBinError(ibin) / float(mc_error_contribution.GetBinContent(ibin))
                else:
                    rel_unc = 0 # for empty bins
                mc_error_contribution.SetBinContent(ibin, 1)
                mc_error_contribution.SetBinError(ibin, rel_unc)

            h_ratio = h_data.Clone("h_ratio")
            h_ratio.SetLineColor(ROOT.kBlack)
            h_ratio.Divide(h_mc_no_errors)

	    h_data.SetLineColor(1)
	    h_mc.SetLineColor(7)

	    h_mc.GetXaxis().SetLabelSize(0)
            h_mc.GetYaxis().SetTitleFont(43)
	    h_mc.GetYaxis().SetTitleOffset(1.7)
	    h_mc.GetYaxis().SetLabelFont(43)
            h_mc.GetYaxis().SetTitleSize(27)
            h_mc.GetYaxis().SetTitleFont(43)
            h_mc.GetYaxis().SetLabelSize(23)

    	    c = ROOT.TCanvas("c1", "c1", 800, 900)
    	    pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
    	    pad1.SetBottomMargin(0.04)  #Upper and lower plot are joined
    	    pad1.SetLeftMargin(0.12)  
    	    pad1.Draw()              #Draw the upper pad: pad1
    	    pad1.cd()                #pad1 becomes the current pad

    	    h_mc.Draw("EHIST")
    	    h_data.Draw("SAME EHIST")

    	    #Lower plot
    	    c.cd() #Go back to main canvas
    	    pad2 = ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.3) 
    	    pad2.SetTopMargin(0.035)
    	    pad2.SetBottomMargin(0.335)
    	    pad2.SetLeftMargin(0.12)
    	    pad2.Draw()
    	    pad2.cd()  #pad2 becomes the current pad

	    h_ratio.GetYaxis().SetTitle("Data/MC")
            h_ratio.GetYaxis().SetNdivisions(505)
            h_ratio.GetYaxis().SetTitleFont(43)
            h_ratio.GetYaxis().SetTitleOffset(1.55)
            h_ratio.GetYaxis().SetLabelFont(43)
            h_ratio.GetYaxis().SetTitleSize(27)
            h_ratio.GetYaxis().SetLabelSize(23)

            h_ratio.GetXaxis().SetTitleFont(43)
            h_ratio.GetXaxis().SetTitleOffset(4.)
            h_ratio.GetXaxis().SetLabelFont(43)
            h_ratio.GetXaxis().SetTitleSize(27)
            h_ratio.GetXaxis().SetLabelSize(23)



    	    h_ratio.SetMarkerStyle(8)
    	    h_ratio.Draw("EP")
	    line = ROOT.TLine(float(h_ratio.GetXaxis().GetXmin()), 1, float(h_ratio.GetXaxis().GetXmax()), 1)
            line.SetLineColor(ROOT.kBlack)
            line.SetLineStyle(2)
            line.Draw("SAME")


    	    #line = ROOT.TLine(float(xmin), 1, float(xmax), 1)
    	    #line.SetLineColor(ROOT.kBlack)
    	    #line.SetLineStyle(2)
    	    #line.Draw("SAME")
    	    c.Print( '%s/%s_ratio/%s.png' % (plotDir, i, tnpBins['bins'][ib]['name'])) 
                 

    #	h_mc = mcSample.Get('%s_Pair' % tnpBins['bins'][ib]['name'] ) 

    #    h_data.Scale(1.0 / h_data.Integral())
    #    h_mc.Scale(1.0 / h_mc.Integral())

    #    h_data.SetLineColor(1)
    #    h_mc.SetLineColor(7)

    #    h_mc.GetYaxis().SetTitleFont(43)
    #    h_mc.GetYaxis().SetTitleOffset(1.7)
    #    h_mc.GetYaxis().SetLabelFont(43)
    #    h_mc.GetYaxis().SetTitleSize(27)
    #    h_mc.GetYaxis().SetTitleFont(43)
    #    h_mc.GetYaxis().SetLabelSize(23)

    #    h_mc.GetXaxis().SetTitleFont(43)
    #    h_mc.GetXaxis().SetTitleOffset(1.7)
    #    h_mc.GetXaxis().SetLabelFont(43)
    #    h_mc.GetXaxis().SetTitleSize(27)
    #    h_mc.GetXaxis().SetTitleFont(43)
    #    h_mc.GetXaxis().SetLabelSize(23)

    #	c = ROOT.TCanvas("c1", "c1", 800, 900)
    #	pad1 = ROOT.TPad("pad1", "pad1", 0, 0.1, 1, 1.0)
    #	pad1.SetBottomMargin(0.04)  #Upper and lower plot are joined
    #	pad1.SetLeftMargin(0.12)  
    #	pad1.Draw()              #Draw the upper pad: pad1
    #	pad1.cd()                #pad1 becomes the current pad

    #	h_mc.Draw("EHIST")
    #	h_data.Draw("SAME EHIST")

    #	c.Print( '%s/pair_mass/%s.png' % (plotDir,tnpBins['bins'][ib]['name'])) 
                 
def doRatios(h_mc, h_data):

    h_data.Scale(1.0 / h_data.Integral())
    h_mc.Scale(1.0 / h_mc.Integral())
    
    h_data.SetStats(0)
    h_mc.SetStats(0)
    
    h_mc_no_errors = h_mc.Clone()
    for ibin in range(h_mc_no_errors.GetNbinsX()+2):
            h_mc_no_errors.SetBinError(ibin, 0)
    
    mc_error_contribution = h_mc.Clone()
    for ibin in range(mc_error_contribution.GetNbinsX()+2):
        if mc_error_contribution.GetBinContent(ibin) != 0:
            rel_unc = mc_error_contribution.GetBinError(ibin) / float(mc_error_contribution.GetBinContent(ibin))
        else:
            rel_unc = 0 # for empty bins
        mc_error_contribution.SetBinContent(ibin, 1)
        mc_error_contribution.SetBinError(ibin, rel_unc)
    
    h_ratio = h_data.Clone("h_ratio")
    h_ratio.SetLineColor(ROOT.kBlack)
    h_ratio.Divide(h_mc_no_errors)
    
    h_data.SetLineColor(1)
    h_mc.SetLineColor(7)
    
    h_mc.GetXaxis().SetLabelSize(0)
    h_mc.GetYaxis().SetTitleFont(43)
    h_mc.GetYaxis().SetTitleOffset(1.7)
    h_mc.GetYaxis().SetLabelFont(43)
    h_mc.GetYaxis().SetTitleSize(27)
    h_mc.GetYaxis().SetTitleFont(43)
    h_mc.GetYaxis().SetLabelSize(23)
    
    c = ROOT.TCanvas("c1", "c1", 800, 900)
    pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
    pad1.SetBottomMargin(0.04)  #Upper and lower plot are joined
    pad1.SetLeftMargin(0.12)  
    pad1.Draw()              #Draw the upper pad: pad1
    pad1.cd()                #pad1 becomes the current pad
    
    h_mc.Draw("EHIST")
    h_data.Draw("SAME EHIST")
    
    #Lower plot
    c.cd() #Go back to main canvas
    pad2 = ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.3) 
    pad2.SetTopMargin(0.035)
    pad2.SetBottomMargin(0.335)
    pad2.SetLeftMargin(0.12)
    pad2.Draw()
    pad2.cd()  #pad2 becomes the current pad
    
    h_ratio.GetYaxis().SetTitle("Data/MC")
    h_ratio.GetYaxis().SetNdivisions(505)
    h_ratio.GetYaxis().SetTitleFont(43)
    h_ratio.GetYaxis().SetTitleOffset(1.55)
    h_ratio.GetYaxis().SetLabelFont(43)
    h_ratio.GetYaxis().SetTitleSize(27)
    h_ratio.GetYaxis().SetLabelSize(23)
    h_ratio.GetYaxis().SetRangeUser(0.5,1.5)
    
    h_ratio.GetXaxis().SetTitleFont(43)
    h_ratio.GetXaxis().SetTitleOffset(4.)
    h_ratio.GetXaxis().SetLabelFont(43)
    h_ratio.GetXaxis().SetTitleSize(27)
    h_ratio.GetXaxis().SetLabelSize(23)
    
    
    
    h_ratio.SetMarkerStyle(8)
    h_ratio.Draw("EP")
    line = ROOT.TLine(float(h_ratio.GetXaxis().GetXmin()), 1, float(h_ratio.GetXaxis().GetXmax()), 1)
    line.SetLineColor(ROOT.kBlack)
    line.SetLineStyle(2)
    line.Draw("SAME")
    
    #line = ROOT.TLine(float(xmin), 1, float(xmax), 1)
    #line.SetLineColor(ROOT.kBlack)
    #line.SetLineStyle(2)
    #line.Draw("SAME")
    c.Print( 'barrel_ratio_mc_sweightd.png')













