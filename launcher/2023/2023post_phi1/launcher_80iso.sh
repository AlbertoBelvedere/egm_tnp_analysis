eval `scram runtime -sh`


python tnpEGM_fitter.py etc/config/settings_ele_2023_postBPIX_phi1.py  --flag passingMVA122Xwp80isoV1 --checkBins

python tnpEGM_fitter.py etc/config/settings_ele_2023_postBPIX_phi1.py  --flag passingMVA122Xwp80isoV1 --createBins

python tnpEGM_fitter.py etc/config/settings_ele_2023_postBPIX_phi1.py  --flag passingMVA122Xwp80isoV1 --createHists

python tnpEGM_fitter.py etc/config/settings_ele_2023_postBPIX_phi1.py  --flag passingMVA122Xwp80isoV1  --doFit 

python tnpEGM_fitter.py etc/config/settings_ele_2023_postBPIX_phi1.py  --flag passingMVA122Xwp80isoV1  --doFit --mcSig --altSig

python tnpEGM_fitter.py etc/config/settings_ele_2023_postBPIX_phi1.py  --flag passingMVA122Xwp80isoV1  --doFit  --altSig

python tnpEGM_fitter.py etc/config/settings_ele_2023_postBPIX_phi1.py  --flag passingMVA122Xwp80isoV1  --doFit  --altBkg

python tnpEGM_fitter.py etc/config/settings_ele_2023_postBPIX_phi1.py  --flag passingMVA122Xwp80isoV1  --sumUp

