eval `scram runtime -sh`



rm -f  results/2023_post_phi1/tnpEleID/passingMVA122Xwp80noisoV1/DY_amcatnlo_passingMVA122Xwp80noisoV1.altSigFit.root
rm -f  results/2023_post_phi1/tnpEleID/passingMVA122Xwp80noisoV1/DY_amcatnlo_passingMVA122Xwp80noisoV1.altSigFit-bin33*
python tnpEGM_fitter.py etc/config/settings_ele_2023_postBPIX_phi1.py  --flag passingMVA122Xwp80noisoV1  --doFit --mcSig  --altSig --iBin 33
rm -f  results/2023_post_phi1/tnpEleID/passingMVA122Xwp80noisoV1/DY_amcatnlo_passingMVA122Xwp80noisoV1.altSigFit.root
rm -f  results/2023_post_phi1/tnpEleID/passingMVA122Xwp80noisoV1/DY_amcatnlo_passingMVA122Xwp80noisoV1.altSigFit-bin34*
python tnpEGM_fitter.py etc/config/settings_ele_2023_postBPIX_phi1.py  --flag passingMVA122Xwp80noisoV1  --doFit --mcSig  --altSig --iBin 34
rm -f  results/2023_post_phi1/tnpEleID/passingMVA122Xwp80noisoV1/DY_amcatnlo_passingMVA122Xwp80noisoV1.altSigFit.root
rm -f  results/2023_post_phi1/tnpEleID/passingMVA122Xwp80noisoV1/DY_amcatnlo_passingMVA122Xwp80noisoV1.altSigFit-bin35*
python tnpEGM_fitter.py etc/config/settings_ele_2023_postBPIX_phi1.py  --flag passingMVA122Xwp80noisoV1  --doFit --mcSig  --altSig --iBin 35
rm -f  results/2023_post_phi1/tnpEleID/passingMVA122Xwp80noisoV1/DY_amcatnlo_passingMVA122Xwp80noisoV1.altSigFit.root
rm -f  results/2023_post_phi1/tnpEleID/passingMVA122Xwp80noisoV1/DY_amcatnlo_passingMVA122Xwp80noisoV1.altSigFit-bin36*
python tnpEGM_fitter.py etc/config/settings_ele_2023_postBPIX_phi1.py  --flag passingMVA122Xwp80noisoV1  --doFit --mcSig  --altSig --iBin 36
rm -f  results/2023_post_phi1/tnpEleID/passingMVA122Xwp80noisoV1/data_2023_passingMVA122Xwp80noisoV1.altSigFit.root
rm -f  results/2023_post_phi1/tnpEleID/passingMVA122Xwp80noisoV1/data_2023_passingMVA122Xwp80noisoV1.altSigFit-bin33*
python tnpEGM_fitter.py etc/config/settings_ele_2023_postBPIX_phi1.py  --flag passingMVA122Xwp80noisoV1  --doFit  --altSig --iBin 33
rm -f  results/2023_post_phi1/tnpEleID/passingMVA122Xwp80noisoV1/data_2023_passingMVA122Xwp80noisoV1.altSigFit.root
rm -f  results/2023_post_phi1/tnpEleID/passingMVA122Xwp80noisoV1/data_2023_passingMVA122Xwp80noisoV1.altSigFit-bin34*
python tnpEGM_fitter.py etc/config/settings_ele_2023_postBPIX_phi1.py  --flag passingMVA122Xwp80noisoV1  --doFit  --altSig --iBin 34
rm -f  results/2023_post_phi1/tnpEleID/passingMVA122Xwp80noisoV1/data_2023_passingMVA122Xwp80noisoV1.altSigFit.root
rm -f  results/2023_post_phi1/tnpEleID/passingMVA122Xwp80noisoV1/data_2023_passingMVA122Xwp80noisoV1.altSigFit-bin35*
python tnpEGM_fitter.py etc/config/settings_ele_2023_postBPIX_phi1.py  --flag passingMVA122Xwp80noisoV1  --doFit  --altSig --iBin 35
rm -f  results/2023_post_phi1/tnpEleID/passingMVA122Xwp80noisoV1/data_2023_passingMVA122Xwp80noisoV1.altSigFit.root
rm -f  results/2023_post_phi1/tnpEleID/passingMVA122Xwp80noisoV1/data_2023_passingMVA122Xwp80noisoV1.altSigFit-bin36*
python tnpEGM_fitter.py etc/config/settings_ele_2023_postBPIX_phi1.py  --flag passingMVA122Xwp80noisoV1  --doFit  --altSig --iBin 36

python tnpEGM_fitter.py etc/config/settings_ele_2023_postBPIX_phi1.py  --flag passingMVA122Xwp80noisoV1  --sumUp

