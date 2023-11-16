eval `scram runtime -sh`


python tnpEGM_fitter.py etc/config/settings_ele_Run3_postleak.py  --flag passingCutBasedVeto122XV1 --flag2 passingCutBasedVetoRun3V1 --checkBins

python tnpEGM_fitter.py etc/config/settings_ele_Run3_postleak.py  --flag passingCutBasedVeto122XV1 --flag2 passingCutBasedVetoRun3V1 --createBins

python tnpEGM_fitter.py etc/config/settings_ele_Run3_postleak.py  --flag passingCutBasedVeto122XV1 --flag2 passingCutBasedVetoRun3V1 --createHists

bash hadding.sh passingCutBasedVeto122XV1 

python tnpEGM_fitter.py etc/config/settings_ele_Run3_postleak.py  --flag passingCutBasedVeto122XV1  --doFit 

#python tnpEGM_fitter.py etc/config/settings_ele_Run3_postleak.py  --flag passingCutBasedVeto122XV1  --doFit  --altSig

python tnpEGM_fitter.py etc/config/settings_ele_Run3_postleak.py  --flag passingCutBasedVeto122XV1  --doFit  --altBkg

python tnpEGM_fitter.py etc/config/settings_ele_Run3_postleak.py  --flag passingCutBasedVeto122XV1  --sumUp

