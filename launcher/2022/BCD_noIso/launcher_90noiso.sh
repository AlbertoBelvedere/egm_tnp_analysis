eval `scram runtime -sh`


python tnpEGM_fitter.py etc/config/settings_ele_Run3_preleak_noIso.py  --flag passingMVA122Xwp90noisoV1 --checkBins

python tnpEGM_fitter.py etc/config/settings_ele_Run3_preleak_noIso.py  --flag passingMVA122Xwp90noisoV1 --createBins

python tnpEGM_fitter.py etc/config/settings_ele_Run3_preleak_noIso.py  --flag passingMVA122Xwp90noisoV1 --createHists

python tnpEGM_fitter.py etc/config/settings_ele_Run3_preleak_noIso.py  --flag passingMVA122Xwp90noisoV1  --doFit 

python tnpEGM_fitter.py etc/config/settings_ele_Run3_preleak_noIso.py  --flag passingMVA122Xwp90noisoV1  --doFit --mcSig --altSig

python tnpEGM_fitter.py etc/config/settings_ele_Run3_preleak_noIso.py  --flag passingMVA122Xwp90noisoV1  --doFit  --altSig

python tnpEGM_fitter.py etc/config/settings_ele_Run3_preleak_noIso.py  --flag passingMVA122Xwp90noisoV1  --doFit  --altBkg

python tnpEGM_fitter.py etc/config/settings_ele_Run3_preleak_noIso.py  --flag passingMVA122Xwp90noisoV1  --sumUp

