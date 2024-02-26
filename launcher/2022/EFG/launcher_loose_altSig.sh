eval `scram runtime -sh`


python tnpEGM_fitter.py etc/config/settings_ele_Run3_postleak_altSig.py  --flag passingCutBasedLoose122XV1  --checkBins

python tnpEGM_fitter.py etc/config/settings_ele_Run3_postleak_altSig.py  --flag passingCutBasedLoose122XV1  --createBins

python tnpEGM_fitter.py etc/config/settings_ele_Run3_postleak_altSig.py  --flag passingCutBasedLoose122XV1  --createHists

python tnpEGM_fitter.py etc/config/settings_ele_Run3_postleak_altSig.py  --flag passingCutBasedLoose122XV1  --doFit 

python tnpEGM_fitter.py etc/config/settings_ele_Run3_postleak_altSig.py  --flag passingCutBasedLoose122XV1  --doFit --mcSig --altSig

python tnpEGM_fitter.py etc/config/settings_ele_Run3_postleak_altSig.py  --flag passingCutBasedLoose122XV1  --doFit  --altSig

python tnpEGM_fitter.py etc/config/settings_ele_Run3_postleak_altSig.py  --flag passingCutBasedLoose122XV1  --doFit  --altBkg

python tnpEGM_fitter.py etc/config/settings_ele_Run3_postleak_altSig.py  --flag passingCutBasedLoose122XV1  --sumUp

