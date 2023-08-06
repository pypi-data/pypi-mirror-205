# NNFal

A neural network-based falsification framework for falsifying several CPS models such as hybrid automata models and Simulink models. The algorithm accepts two inputs a safety property and a neural network model that acts as an approximation model of the CPS models. It includes the DNNF, neural network falsifier tool for obtaining counterexample input. XSpeed is used for validating the counterexample for hybrid automata models and the counterexample input of Simulink model is varified using the MATLAB. 


# Prerequisites
NNFal requires the following libraries...

	- DNNF for generating the CE inputs.
		[https://github.com/dlshriver/dnnf]

	- XSpeed for simulating and validating the hybrid automata models.
		[https://gitlab.com/Atanukundu/XSpeed-plan]
		
	- MATLAB for simulating and validating the state-flow/Simulink models.
		[https://in.mathworks.com/products/simulink.html]
		
	- MATLAB Engine for python. From a python script we can call simulink model through MATLAB Engine API.
		[https://in.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html]
		
To install the above prerequisites just run the install.sh file
		
# Installation
	
- Allow default installation of the library header files into the directory /usr/local/include and the .a/.so files into the directory /usr/local/lib.

- clone XSpeed repository into the validation directory of NNFal and built it from source(Instructions are given in the XSpeed repo). 

# For ARCH-COMP to get result

cd source
python3 run_matlab.py

# Run

- Run command <bash measure_all> in the NNFal/source directory. It automatically strore the result in .csv file in the same directory.

	Additional python libraries and runlim required to run the <measure_all> script.
	
	
# Author and Contact

	Atanu Kundu
	E-mail: mcsak2346@iacs.res.in


