#############################################################
########## General settings
#############################################################
# flag to be Tested
cutpass80 = '(( abs(probe_sc_eta) < 0.8 && probe_Ele_nonTrigMVA > %f ) ||  ( abs(probe_sc_eta) > 0.8 && abs(probe_sc_eta) < 1.479&& probe_Ele_nonTrigMVA > %f ) || ( abs(probe_sc_eta) > 1.479 && probe_Ele_nonTrigMVA > %f ) )' % (0.967083,0.929117,0.726311)
cutpass90 = '(( abs(probe_sc_eta) < 0.8 && probe_Ele_nonTrigMVA > %f ) ||  ( abs(probe_sc_eta) > 0.8 && abs(probe_sc_eta) < 1.479&& probe_Ele_nonTrigMVA > %f ) || ( abs(probe_sc_eta) > 1.479 && probe_Ele_nonTrigMVA > %f ) )' % (0.913286,0.805013,0.358969)

# flag to be Tested
flags = {
    'passingCutBasedVeto94XV2'    : '(passingCutBasedVeto94XV2   == 1)',
    'passingCutBasedLoose94XV2'   : '(passingCutBasedLoose94XV2  == 1)',
    'passingCutBasedMedium94XV2'  : '(passingCutBasedMedium94XV2 == 1)',
    'passingCutBasedTight94XV2'   : '(passingCutBasedTight94XV2  == 1)',
    'passingMVA94Xwp80isoV2' : '(passingMVA94Xwp80isoV2 == 1)',
    'passingMVA94Xwp90isoV2' : '(passingMVA94Xwp90isoV2 == 1)',
    'passingMVA94Xwp80noisoV2' : '(passingMVA94Xwp80noisoV2 == 1)',
    'passingMVA94Xwp90noisoV2' : '(passingMVA94Xwp90noisoV2 == 1)',
    'passingCutBasedVeto122XV1'    : '(passingCutBasedVeto122XV1 == 1)',
    'passingCutBasedLoose122XV1'    : '(passingCutBasedLoose122XV1 == 1)',
    'passingCutBasedMedium122XV1'    : '(passingCutBasedMedium122XV1 == 1)',
    'passingCutBasedTight122XV1'    : '(passingCutBasedTight122XV1 == 1)',
    'passingMVA122Xwp80isoV1'    : '(passingMVA122Xwp80isoV1 == 1)',
    'passingMVA122Xwp80noisoV1'    : '(passingMVA122Xwp80noisoV1 == 1)',
    'passingMVA122Xwp90isoV1'    : '(passingMVA122Xwp90isoV1 == 1)',
    'passingMVA122Xwp90noisoV1'    : '(passingMVA122Xwp90noisoV1 == 1)',
    'passingCutBasedVetoRun3V1'    : '(passingCutBasedVetoRun3V1 == 1)',
    'passingCutBasedLooseRun3V1'    : '(passingCutBasedLooseRun3V1 == 1)',
    'passingCutBasedMediumRun3V1'    : '(passingCutBasedMediumRun3V1 == 1)',
    'passingCutBasedTightRun3V1'    : '(passingCutBasedTightRun3V1 == 1)',
    'passingMVARun3Xwp80isoV1'    : '(passingMVARun3Xwp80isoV1 == 1)',
    'passingMVARun3Xwp80noisoV1'    : '(passingMVARun3Xwp80noisoV1 == 1)',
    'passingMVARun3Xwp90isoV1'    : '(passingMVARun3Xwp90isoV1 == 1)',
    'passingMVARun3Xwp90noisoV1'    : '(passingMVARun3Xwp90noisoV1 == 1)',
    }

baseOutDir = 'results/2023_post_phi1/tnpEleID/'

#############################################################
########## samples definition  - preparing the samples
#############################################################
### samples are defined in etc/inputs/tnpSampleDef.py
### not: you can setup another sampleDef File in inputs
import etc.inputs.tnpSampleDef as tnpSamples
tnpTreeDir = 'tnpEleIDs'

samplesDef = {
    'data'   : tnpSamples.Run3_2023_post['data_2023'].clone(),
    'mcNom'  : tnpSamples.Run3_2023_post['DY_amcatnlo'].clone(),
    'mcAlt'  : tnpSamples.Run3_2023_post['DY_madgraph'].clone(),
    'tagSel' : tnpSamples.Run3_2023_post['DY_amcatnlo'].clone(),
}

## can add data sample easily
#samplesDef['data'].add_sample( tnpSamples.Run3_postleak['data_Run3F'] )
#samplesDef['data'].add_sample( tnpSamples.Run3_postleak['data_Run3G'] )

## some sample-based cuts... general cuts defined here after
## require mcTruth on MC DY samples and additional cuts
## all the samples MUST have different names (i.e. sample.name must be different for all)
## if you need to use 2 times the same sample, then rename the second one
#samplesDef['data'  ].set_cut('run >= 273726')
samplesDef['data' ].set_tnpTree(tnpTreeDir)
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_tnpTree(tnpTreeDir)
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_tnpTree(tnpTreeDir)
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_tnpTree(tnpTreeDir)

if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_mcTruth()
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_mcTruth()
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_mcTruth()
if not samplesDef['tagSel'] is None:
    samplesDef['tagSel'].rename('mcAltSel_DY_madgraph')
    samplesDef['tagSel'].set_cut('tag_Ele_pt > 35') #canceled non trig MVA cut


## set MC weight, can use several pileup rw for different data taking periods
#weightName = 'weights_data_Run2022_B-G.totWeight'
weightName = 'weights_data_Run2023D.totWeight'
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_weight(weightName)
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_weight(weightName)
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_weight(weightName)
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_puTree('/eos/cms/store/group/phys_egamma/ec/tnpTuples/Prompt2023/pileupReweightingFiles/postBPIX/DY_amcatnloext_ele.pu.puTree.root')
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_puTree('/eos/cms/store/group/phys_egamma/ec/tnpTuples/Prompt2023/pileupReweightingFiles/postBPIX/DY_madgraph_ele.pu.puTree.root')
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_puTree('/eos/cms/store/group/phys_egamma/ec/tnpTuples/Prompt2023/pileupReweightingFiles/postBPIX/DY_amcatnloext_ele.pu.puTree.root')

#############################################################
########## bining definition  [can be nD bining]
#############################################################
biningDef = [
   { 'var' : 'el_sc_eta' , 'type': 'float', 'bins': [-2.5,-2.0,-1.566,-1.4442, -0.8, 0.0, 0.8, 1.4442, 1.566, 2.0, 2.5] },
   { 'var' : 'el_pt' , 'type': 'float', 'bins': [10,20,35,50,100,500] },
]

#############################################################
########## Cuts definition for all samples
#############################################################
### cut
cutBase   = 'tag_Ele_pt > 33 && abs(tag_sc_eta) < 2.17 && el_q*tag_Ele_q < 0 && ( (el_sc_eta>=0 || el_sc_eta<= -1.5) || (el_sc_eta<0 && el_sc_eta>-1.5 && (el_phi<-0.8 && el_phi>-1.2)))'

additionalCuts = { 
    0 : 'tag_Ele_Iso122X > 0.90 ',
    1 : 'tag_Ele_Iso122X > 0.90 ',
    2 : 'tag_Ele_Iso122X > 0.90 ',
    3 : 'tag_Ele_Iso122X > 0.90 ',
    4 : 'tag_Ele_Iso122X > 0.90 ',
    5 : 'tag_Ele_Iso122X > 0.90 ',
    6 : 'tag_Ele_Iso122X > 0.90 ',
    7 : 'tag_Ele_Iso122X > 0.90 ',
    8 : 'tag_Ele_Iso122X > 0.90 ',
    9 : 'tag_Ele_Iso122X > 0.90 '
}

#### or remove any additional cut (default)
#additionalCuts = None

#############################################################
########## fitting params to tune fit by hand if necessary
#############################################################
#tnpParNomFit = [
#    "meanP[-0.0,-5.0,5.0]","sigmaP[0.9,0,5.0]",
#    "meanF[-0.0,-5.0,5.0]","sigmaF[0.9,0,5.0]",
#    "acmsP[60.,30.,100.]","betaP[0.05,0.001,0.08]","gammaP[0.1, -2, 2]","peakP[90.0]",
#    "acmsF[60.,30,80.]","betaF[0.05,0.001,0.12]","gammaF[0.1, -2, 2]","peakF[90.0]",
#    ]
tnpParNomFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.9,0,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.9,0,5.0]",
    "acmsP[60.,30.,100.]","betaP[0.05,0.001,0.08]","gammaP[0.1, -0.1, 0.1]","peakP[90.0]",
    "acmsF[60.,30,80.]","betaF[0.05,0.001,0.12]","gammaF[0.1, -2, 2]","peakF[90.0]",
    ]

#general
tnpParAltSigFit = [
    "meanP[-0.0,-2.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    "meanF[-0.0,-3.0,5.0]","sigmaF[0.5,0.7,6.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    "acmsP[60.,50.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    "acmsF[60.,50.,75.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
    ]

#35-50pt
tnpParAltSigFit3550 = [
    "meanP[0.0, -2.,2.5]","sigmaP[1.5,0.1,3.0]","alphaP[1.0,0,2.]" ,'nP[0.75,0.1,1.5]',"sigmaP_2[1.5,0.1,2.0]","sosP[1,0.01,5.0]",
    "meanF[0.0, -2.,2.5]","sigmaF[2,0.1,3.0]","alphaF[1.0,0,2.]",'nF[0.75,0.1,1.5]',"sigmaF_2[2.,0.1,2.0]","sosF[1,0.01,2.0]",
    "acmsP[60.,50.,75.]","betaP[0.06,0.01,0.06]","gammaP[0.005, 0.001, 0.8]","peakP[90.0]",
    "acmsF[75.,50.,250.]","betaF[0.06,0.01,0.06]","gammaF[0.005, 0.001, 0.9]","peakF[90.0]",
    ]

#50-100pt
tnpParAltSigFit50100 = [
    "meanP[1.0, 0.1,2.5]","sigmaP[1.5,0.1,2.0]","alphaP[-0.8,-1.5,0.5]" ,'nP[0.75,0.1,1.5]',"sigmaP_2[1.5,0.1,2.0]","sosP[1,0.01,5.0]",
    "meanF[1.0, 0.1,2.5]","sigmaF[1.5,0.1,2.0]","alphaF[-0.8,-1.5,0.5]",'nF[0.75,0.1,1.5]',"sigmaF_2[2.,0.1,2.0]","sosF[1,0.01,3.0]",
    "acmsP[75.,50.,250.]","betaP[0.06,0.01,0.06]","gammaP[0.005, 0., 1]","peakP[90.0]",
    "acmsF[75.,50.,250.]","betaF[0.06,0.01,0.06]","gammaF[0.005, 0., 1]","peakF[90.0]",
    ]

#100-500pt
tnpParAltSigFit100500 = [
    "meanP[-0.0,-2.0,3.0]","sigmaP[1,0.7,3.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.,0.5,2.0]","sosP[1,0.5,5.0]",
    "meanF[-0.0,-3.0,3.0]","sigmaF[0.5,0.7,3.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[1.0,0.5,2.0]","sosF[1,0.5,5.0]",
    "acmsP[75.,50.,250.]","betaP[0.06,0.01,0.06]","gammaP[0.005, 0., 1]","peakP[90.0]",
    "acmsF[75.,50.,250.]","betaF[0.036]","gammaF[0.005, 0., 0.1]","peakF[90.0]",
    ]

tnpParAltSigFit_addGaus = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,6.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    "meanGF[80.0,70.0,100.0]","sigmaGF[15,5.0,125.0]",
    "acmsP[60.,50.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    "acmsF[60.,50.,75.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
    ]
         
tnpParAltBkgFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.9,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.9,0.5,3.0]",
    "alphaP[0.,-5.,5.]",
    "alphaF[0.,-5.,5.]",
    ]
