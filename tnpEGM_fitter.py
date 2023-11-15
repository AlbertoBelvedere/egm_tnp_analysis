
### python specific import
import argparse
import os
import sys
import pickle
import shutil
import ROOT
from multiprocessing import Pool


parser = argparse.ArgumentParser(description='tnp EGM fitter')
parser.add_argument('--checkBins'  , action='store_true'  , help = 'check  bining definition')
parser.add_argument('--createBins' , action='store_true'  , help = 'create bining definition')
parser.add_argument('--createHists', action='store_true'  , help = 'create histograms')
parser.add_argument('--sample'     , default='all'        , help = 'create histograms (per sample, expert only)')
parser.add_argument('--altSig'     , action='store_true'  , help = 'alternate signal model fit')
parser.add_argument('--addGaus'    , action='store_true'  , help = 'add gaussian to alternate signal model failing probe')
parser.add_argument('--altBkg'     , action='store_true'  , help = 'alternate background model fit')
parser.add_argument('--doFit'      , action='store_true'  , help = 'fit sample (sample should be defined in settings.py)')
parser.add_argument('--mcSig'      , action='store_true'  , help = 'fit MC nom [to init fit parama]')
parser.add_argument('--contSFs'	   , action='store_true'  , help = 'compute continuos SFs')
parser.add_argument('--Sweights'   , action='store_true'  , help = 'compute Sweights')
parser.add_argument('--doSweightsplot'   , action='store_true'  , help = 'plot Sweights histos')
parser.add_argument('--doPlot'     , action='store_true'  , help = 'plotting')
parser.add_argument('--sumUp'      , action='store_true'  , help = 'sum up efficiencies')
parser.add_argument('--iBin'       , dest = 'binNumber'   , type = int,  default=-1, help='bin number (to refit individual bin)')
parser.add_argument('--flag'       , default = None       , help ='WP to test')
parser.add_argument('settings'     , default = None       , help = 'setting file [mandatory]')


args = parser.parse_args()

print '===> settings %s <===' % args.settings
importSetting = 'import %s as tnpConf' % args.settings.replace('/','.').split('.py')[0]
print importSetting
exec(importSetting)

### tnp library
import libPython.binUtils  as tnpBiner
import libPython.rootUtils as tnpRoot
import libPython.rootUtils_MVA as tnpRoot_MVA


if args.flag is None:
    print '[tnpEGM_fitter] flag is MANDATORY, this is the working point as defined in the settings.py'
    sys.exit(0)
    
if not args.flag in tnpConf.flags.keys() :
    print '[tnpEGM_fitter] flag %s not found in flags definitions' % args.flag
    print '  --> define in settings first'
    print '  In settings I found flags: '
    print tnpConf.flags.keys()
    sys.exit(1)

outputDirectory = '%s/%s/' % (tnpConf.baseOutDir,args.flag)

print '===>  Output directory: '
print outputDirectory


####################################################################
##### Create (check) Bins
####################################################################
if args.checkBins:
    tnpBins = tnpBiner.createBins(tnpConf.biningDef,tnpConf.cutBase)
    tnpBiner.tuneCuts( tnpBins, tnpConf.additionalCuts )
    for ib in range(len(tnpBins['bins'])):
        print tnpBins['bins'][ib]['name']
        print '  - cut: ',tnpBins['bins'][ib]['cut']
    sys.exit(0)
    
if args.createBins:
    if os.path.exists( outputDirectory ):
            shutil.rmtree( outputDirectory )
    os.makedirs( outputDirectory )
    tnpBins = tnpBiner.createBins(tnpConf.biningDef,tnpConf.cutBase)
    tnpBiner.tuneCuts( tnpBins, tnpConf.additionalCuts )
    pickle.dump( tnpBins, open( '%s/bining.pkl'%(outputDirectory),'wb') )
    print 'created dir: %s ' % outputDirectory
    print 'bining created successfully... '
    print 'Note than any additional call to createBins will overwrite directory %s' % outputDirectory
    sys.exit(0)

tnpBins = pickle.load( open( '%s/bining.pkl'%(outputDirectory),'rb') )


####################################################################
##### Create Histograms
####################################################################
for s in tnpConf.samplesDef.keys():
    sample =  tnpConf.samplesDef[s]
    if sample is None: continue
    setattr( sample, 'tree'     ,'%s/fitter_tree' % tnpConf.tnpTreeDir )
    setattr( sample, 'histFile' , '%s/%s_%s.root' % ( outputDirectory , sample.name, args.flag ) )
    setattr( sample, 'histRatioFile' , '%s/%s_%s.root' % ( outputDirectory , "ratioHistograms", args.flag) )


if args.createHists:

    import libPython.histUtils_MVA as tnpHist_MVA

    for i in tnpConf.samplesDef.keys():
	if  ((i == 'mcNom') | (i == 'data')):
    	   sample =  tnpConf.samplesDef[i]
    	   if sample is None : sys.exit(0)
    	   if i == args.sample or args.sample == 'all' :
    	       print 'creating histogram for sample '
    	       sample.dump()
    	       var = { 'name' : 'pair_mass', 'nbins' : 80, 'min' : 60, 'max': 120 }
    	       if sample.mcTruth:
    	           var = { 'name' : 'pair_mass', 'nbins' : 80, 'min' : 60, 'max': 120 }
    	       tnpHist_MVA.makePassFailHistograms( sample, tnpConf.flags[args.flag], tnpBins, var )
	else: 
	   continue


    #import libPython.histUtils as tnpHist

    #def parallel_hists(sampleType):
    #    sample =  tnpConf.samplesDef[sampleType]
    #    if sample is None : return
    #    if sampleType == args.sample or args.sample == 'all' :
    #        print 'creating histogram for sample '
    #        sample.dump()
    #        var = { 'name' : 'pair_mass', 'nbins' : 80, 'min' : 50, 'max': 130 }
    #        if sample.mcTruth:
    #            var = { 'name' : 'pair_mass', 'nbins' : 80, 'min' : 50, 'max': 130 }
    #        tnpHist.makePassFailHistograms( sample, tnpConf.flags[args.flag], tnpBins, var )
    #
    #pool = Pool()
    #pool.map(parallel_hists, tnpConf.samplesDef.keys())

    #sys.exit(0)


####################################################################
##### Make ratios
####################################################################
if args.contSFs:
   setattr( sample, 'hMVA_data' , '%s/%s_%s.root' % ( outputDirectory , tnpConf.samplesDef['data'].name, args.flag ) )
   setattr( sample, 'hMVA_mc' , '%s/%s_%s.root' % ( outputDirectory , tnpConf.samplesDef['mcNom'].name, args.flag) )
#   dataSample = tnpConf.samplesDef['data']
#   mcSample = tnpConf.samplesDef['mcNom']
#   
#   dataSample.dump()
#   mcSample.dump()

   dataSample = ROOT.TFile(sample.hMVA_data, "read")
   mcSample = ROOT.TFile(sample.hMVA_mc, "read")

   outfile = ROOT.TFile(sample.histRatioFile, 'recreate')
   
   hRatio = []

   for ib in range(len(tnpBins['bins'])):
      hMVA_data = dataSample.Get('%s_MVA' % tnpBins['bins'][ib]['name'] ) 
      hMVA_mc = mcSample.Get('%s_MVA' % tnpBins['bins'][ib]['name'] ) 
   
      hMVA_data.Scale(1.0 / hMVA_data.Integral())
      hMVA_mc.Scale(1.0 / hMVA_mc.Integral())

      hRatio.append(hMVA_data.Clone("ratio hist"))

      hRatio[ib].Divide(hMVA_mc)

      hRatio[ib].Write('%s_ratio' % tnpBins['bins'][ib]['name'])

   outfile.Close() 
   setattr( sample, 'hMVA_ratio' , '%s/%s_%s.root' % ( outputDirectory , 'ratioHistograms', args.flag) )

   from libPython.makeCanvas import makeCanvas
   plottingDir = '%s/plots/' % (outputDirectory)
   if not os.path.exists( plottingDir ):
       os.makedirs( plottingDir )
       
   makeCanvas(sample, tnpBins, plottingDir)  



####################################################################
##### Actual Fitter
####################################################################
sampleToFit = tnpConf.samplesDef['data']
if sampleToFit is None:
    print '[tnpEGM_fitter, prelim checks]: sample (data or MC) not available... check your settings'
    sys.exit(1)

sampleMC = tnpConf.samplesDef['mcNom']

if sampleMC is None:
    print '[tnpEGM_fitter, prelim checks]: MC sample not available... check your settings'
    sys.exit(1)
for s in tnpConf.samplesDef.keys():
    sample =  tnpConf.samplesDef[s]
    if sample is None: continue
    setattr( sample, 'mcRef'     , sampleMC )
    setattr( sample, 'nominalFit', '%s/%s_%s.nominalFit.root' % ( outputDirectory , sample.name, args.flag ) )
    setattr( sample, 'altSigFit' , '%s/%s_%s.altSigFit.root'  % ( outputDirectory , sample.name, args.flag ) )
    setattr( sample, 'altBkgFit' , '%s/%s_%s.altBkgFit.root'  % ( outputDirectory , sample.name, args.flag ) )



### change the sample to fit is mc fit
if args.mcSig :
    sampleToFit = tnpConf.samplesDef['mcNom']

if  args.doFit:
    sampleToFit.dump()
    #def parallel_fit(ib):
    #    if (args.binNumber >= 0 and ib == args.binNumber) or args.binNumber < 0:

    for ib in range(0, len(tnpBins['bins'])):
    	#if args.altSig and not args.addGaus:
    	#    tnpRoot.histFitterAltSig(  sampleToFit, tnpBins['bins'][ib], tnpConf.tnpParAltSigFit )
    	#elif args.altSig and args.addGaus:
    	#    tnpRoot.histFitterAltSig(  sampleToFit, tnpBins['bins'][ib], tnpConf.tnpParAltSigFit_addGaus, 1)
    	#elif args.altBkg:
    	#    tnpRoot.histFitterAltBkg(  sampleToFit, tnpBins['bins'][ib], tnpConf.tnpParAltBkgFit )
    	#else:
    	tnpRoot_MVA.histFitterNominal( sampleToFit, tnpBins['bins'][ib], tnpConf.tnpParNomFit )
    	#pool = Pool()
    	#pool.map(parallel_fit, range(len(tnpBins['bins'])))

    args.doPlot = True


#####################################################################
###### Actual Fitter
#####################################################################
#sampleToFit = tnpConf.samplesDef['data']
#if sampleToFit is None:
#    print '[tnpEGM_fitter, prelim checks]: sample (data or MC) not available... check your settings'
#    sys.exit(1)
#
#sampleMC = tnpConf.samplesDef['mcNom']
#
#if sampleMC is None:
#    print '[tnpEGM_fitter, prelim checks]: MC sample not available... check your settings'
#    sys.exit(1)
#for s in tnpConf.samplesDef.keys():
#    sample =  tnpConf.samplesDef[s]
#    if sample is None: continue
#    setattr( sample, 'mcRef'     , sampleMC )
#    setattr( sample, 'nominalFit', '%s/%s_%s.nominalFit.root' % ( outputDirectory , sample.name, args.flag ) )
#    setattr( sample, 'altSigFit' , '%s/%s_%s.altSigFit.root'  % ( outputDirectory , sample.name, args.flag ) )
#    setattr( sample, 'altBkgFit' , '%s/%s_%s.altBkgFit.root'  % ( outputDirectory , sample.name, args.flag ) )
#
#
#
#### change the sample to fit is mc fit
#if args.mcSig :
#    sampleToFit = tnpConf.samplesDef['mcNom']
#
#if  args.doFit:
#    sampleToFit.dump()
#    def parallel_fit(ib):
#        if (args.binNumber >= 0 and ib == args.binNumber) or args.binNumber < 0:
#            if args.altSig and not args.addGaus:
#                tnpRoot.histFitterAltSig(  sampleToFit, tnpBins['bins'][ib], tnpConf.tnpParAltSigFit )
#            elif args.altSig and args.addGaus:
#                tnpRoot.histFitterAltSig(  sampleToFit, tnpBins['bins'][ib], tnpConf.tnpParAltSigFit_addGaus, 1)
#            elif args.altBkg:
#                tnpRoot.histFitterAltBkg(  sampleToFit, tnpBins['bins'][ib], tnpConf.tnpParAltBkgFit )
#            else:
#                tnpRoot.histFitterNominal( sampleToFit, tnpBins['bins'][ib], tnpConf.tnpParNomFit )
#    pool = Pool()
#    pool.map(parallel_fit, range(len(tnpBins['bins'])))
#
#    args.doPlot = True
     

####################################################################
##### computing Sweights and MVA distribution
####################################################################

if args.Sweights:
    import libPython.histSweights as Sweights
    
    input_file = "results/UL2018_continuousSF/tnpEleID/passingMVA94Xwp80isoV2/data_Run2018A_passingMVA94Xwp80isoV2.nominalFit-bin09_el_sc_eta_0p00To1p44_el_pt_20p00To35p00.root"
    #input_file = "results/UL2018_continuousSF/tnpEleID/passingMVA94Xwp80isoV2/data_Run2018A_passingMVA94Xwp80isoV2.nominalFit-bin26_el_sc_eta_m1p44To0p00_el_pt_100p00To500p00.root"

    infile = ROOT.TFile.Open(input_file, "READ")

    #results_name = "bin26_el_sc_eta_m1p44To0p00_el_pt_100p00To500p00_resP"
    results_name = "bin09_el_sc_eta_0p00To1p44_el_pt_20p00To35p00_resP"
    roofitresults = infile.Get(results_name)
    # To print the best fit values
    final_param = roofitresults.floatParsFinal()

    #1) RooRealVar::  acmsP = 50.0001 +/- (-6.59713e-05,1.24771)
    #2) RooRealVar::  betaP = 0.0100001 +/- (-1.04069e-07,6.42852e-05)
    #3) RooRealVar:: gammaP = 0.0353873 +/- 0.000147396
    #4) RooRealVar::  meanP = -0.887778 +/- (-0.0131056,0.0127332)
    #5) RooRealVar::  nBkgP = 423089 +/- (-984.382,946.232)
    #6) RooRealVar::  nSigP = 317725 +/- (-892.18,925.965)
    #7) RooRealVar:: sigmaP = 0.995864 +/- (-0.0388924,0.044162)

    #acmsP = final_param[0].getValV() 
    #betaP = final_param[0].getValV() 
    #gammaP = final_param[0].getValV() 
    #meanP = final_param[0].getValV() 
    #BkgP = final_param[0].getValV() 
    #nSigP = final_param[0].getValV() 
    #sigmaP = final_param[0].getValV() 


    alphaP = 1/0.020
    meanP = 90-0.436
    sigmaP = 1.005
    x = 90

    from scipy.stats import norm, expon

    sig_mass = norm(loc = meanP, scale = sigmaP)
    bkg_mass = expon(scale = alphaP)

    import libPython.histUtils_MVA_sweights as tnpHist_MVA_sweights

    for i in tnpConf.samplesDef.keys():
	if  ((i == 'data')):
    	   sample =  tnpConf.samplesDef[i]
    	   if sample is None : sys.exit(0)
    	   if i == args.sample or args.sample == 'all' :
    	       print 'creating histogram for sample '
    	       sample.dump()
    	       var = { 'name' : 'pair_mass', 'nbins' : 80, 'min' : 60, 'max': 120 }
    	       if sample.mcTruth:
    	           var = { 'name' : 'pair_mass', 'nbins' : 80, 'min' : 60, 'max': 120 }
    	       tnpHist_MVA_sweights.makePassFailHistograms( sample, tnpConf.flags[args.flag], tnpBins, var , sig_mass, bkg_mass)
	else: 
	   continue

    #sig_mass.pdf(x)
    #bkg_mass.pdf(x)


if args.doSweightsplot:
   from libPython.makeCanvas import doRatios

   
   setattr( sample, 'hMVA_mc' , '%s/%s_%s.root' % ( outputDirectory , tnpConf.samplesDef['mcNom'].name, args.flag) )

   dataSample = ROOT.TFile("results/UL2018_continuousSF_rightrange/tnpEleID/passingMVA94Xwp80isoV2/data_Run2018A_passingMVA94Xwp80isoV2_sweights.root", "read")
   mcSample = ROOT.TFile(sample.hMVA_mc, "read")
    
   h_data = dataSample.Get('%s_%s' % (tnpBins['bins'][9]['name'], 'MVAsig')) 
   h_mc = mcSample.Get('%s_%s' % (tnpBins['bins'][9]['name'], 'MVA')) 

   doRatios(h_mc, h_data)
   

####################################################################
##### dumping plots
####################################################################
if  args.doPlot:
    fileName = sampleToFit.nominalFit
    fitType  = 'nominalFit'
    if args.altSig : 
        fileName = sampleToFit.altSigFit
        fitType  = 'altSigFit'
    if args.altBkg : 
        fileName = sampleToFit.altBkgFit
        fitType  = 'altBkgFit'
        
    os.system('hadd -f %s %s' % (fileName, fileName.replace('.root', '-*.root')))

    plottingDir = '%s/plots/%s/%s' % (outputDirectory,sampleToFit.name,fitType)
    if not os.path.exists( plottingDir ):
        os.makedirs( plottingDir )
    shutil.copy('etc/inputs/index.php.listPlots','%s/index.php' % plottingDir)

    for ib in range(len(tnpBins['bins'])):
        if (args.binNumber >= 0 and ib == args.binNumber) or args.binNumber < 0:
            tnpRoot.histPlotter( fileName, tnpBins['bins'][ib], plottingDir )

    print ' ===> Plots saved in <======='
#    print 'localhost/%s/' % plottingDir


####################################################################
##### dumping egamma txt file 
####################################################################
if args.sumUp:
    sampleToFit.dump()
    info = {
        'data'        : sampleToFit.histFile,
        'dataNominal' : sampleToFit.nominalFit,
        'dataAltSig'  : sampleToFit.altSigFit ,
        'dataAltBkg'  : sampleToFit.altBkgFit ,
        'mcNominal'   : sampleToFit.mcRef.histFile,
        'mcAlt'       : None,
        'tagSel'      : None
        }

    #if not tnpConf.samplesDef['mcAlt' ] is None:
    #    info['mcAlt'    ] = tnpConf.samplesDef['mcAlt' ].histFile
    if not tnpConf.samplesDef['tagSel'] is None:
        info['tagSel'   ] = tnpConf.samplesDef['tagSel'].histFile

    effis = None
    effFileName ='%s/egammaEffi.txt' % outputDirectory 
    fOut = open( effFileName,'w')
    
    for ib in range(len(tnpBins['bins'])):
        effis = tnpRoot.getAllEffi( info, tnpBins['bins'][ib] )

        ### formatting assuming 2D bining -- to be fixed        
        v1Range = tnpBins['bins'][ib]['title'].split(';')[1].split('<')
        v2Range = tnpBins['bins'][ib]['title'].split(';')[2].split('<')
        if ib == 0 :
            astr = '### var1 : %s' % v1Range[1]
            print astr
            fOut.write( astr + '\n' )
            astr = '### var2 : %s' % v2Range[1]
            print astr
            fOut.write( astr + '\n' )
            
        astr =  '%+8.5f\t%+8.5f\t%+8.5f\t%+8.5f\t%5.5f\t%5.5f\t%5.5f\t%5.5f\t%5.5f\t%5.5f\t%5.5f\t%5.5f' % (
            float(v1Range[0]), float(v1Range[2]),
            float(v2Range[0]), float(v2Range[2]),
            effis['dataNominal'][0],effis['dataNominal'][1],
            effis['mcNominal'  ][0],effis['mcNominal'  ][1],
            effis['dataAltBkg' ][0],
            effis['dataAltSig' ][0],
            effis['mcAlt' ][0],
            effis['tagSel'][0],
            )
        print astr
        fOut.write( astr + '\n' )
    fOut.close()

    print 'Effis saved in file : ',  effFileName
    import libPython.EGammaID_scaleFactors as egm_sf
    egm_sf.doEGM_SFs(effFileName,sampleToFit.lumi)

