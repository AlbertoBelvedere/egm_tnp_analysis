eval `scram runtime -sh`


python tnpEGM_fitter.py etc/config/settings_ele_Run3_postleak.py  --flag passingMVA122Xwp90isoV1 --flag2 passingMVARun3Xwp90isoV1 --checkBins

python tnpEGM_fitter.py etc/config/settings_ele_Run3_postleak.py  --flag passingMVA122Xwp90isoV1 --flag2 passingMVARun3Xwp90isoV1 --createBins

python tnpEGM_fitter.py etc/config/settings_ele_Run3_postleak.py  --flag passingMVA122Xwp90isoV1 --flag2 passingMVARun3Xwp90isoV1 --createHists

bash hadding.sh passingMVA122Xwp90isoV1

python tnpEGM_fitter.py etc/config/settings_ele_Run3_postleak.py  --flag passingMVA122Xwp90isoV1  --doFit 

python tnpEGM_fitter.py etc/config/settings_ele_Run3_postleak.py  --flag passingMVA122Xwp90isoV1  --doFit  --altSig

python tnpEGM_fitter.py etc/config/settings_ele_Run3_postleak.py  --flag passingMVA122Xwp90isoV1  --doFit  --altBkg

python tnpEGM_fitter.py etc/config/settings_ele_Run3_postleak.py  --flag passingMVA122Xwp90isoV1  --sumUp

