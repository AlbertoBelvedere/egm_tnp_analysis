file1="data_Run3E_"$1".root"
file2="data_Run3F_"$1".root"
directory="results/Run3_postleak_new/tnpEleID/"$1

cd $directory 

mv $file1 "temp.root"

hadd $file1 "temp.root" $file2

cd -
