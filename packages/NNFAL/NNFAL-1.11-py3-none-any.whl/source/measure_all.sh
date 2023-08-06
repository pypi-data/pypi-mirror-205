#/bin/sh

#python3 run_xspeed.py

echo "Reproducing results for the NNFal"
cd ./NNFal/source/
echo "Running Simulink models."
python3 run_matlab.py
