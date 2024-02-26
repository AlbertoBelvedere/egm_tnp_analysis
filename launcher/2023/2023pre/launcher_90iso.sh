eval `scram runtime -sh`


python tnpEGM_fitter.py etc/config/settings_ele_2023_preBPIX.py  --flag passingMVA122Xwp90isoV1 --checkBins

python tnpEGM_fitter.py etc/config/settings_ele_2023_preBPIX.py  --flag passingMVA122Xwp90isoV1 --createBins

python tnpEGM_fitter.py etc/config/settings_ele_2023_preBPIX.py  --flag passingMVA122Xwp90isoV1 --createHists

python tnpEGM_fitter.py etc/config/settings_ele_2023_preBPIX.py  --flag passingMVA122Xwp90isoV1  --doFit 

python tnpEGM_fitter.py etc/config/settings_ele_2023_preBPIX.py  --flag passingMVA122Xwp90isoV1  --doFit --mcSig --altSig

python tnpEGM_fitter.py etc/config/settings_ele_2023_preBPIX.py  --flag passingMVA122Xwp90isoV1  --doFit  --altSig

python tnpEGM_fitter.py etc/config/settings_ele_2023_preBPIX.py  --flag passingMVA122Xwp90isoV1  --doFit  --altBkg

python tnpEGM_fitter.py etc/config/settings_ele_2023_preBPIX.py  --flag passingMVA122Xwp90isoV1  --sumUp

