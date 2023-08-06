##!/usr/bin/env python3

import os
import sys

import os
import subprocess
import re
import numpy as np
import xspeed
import dnnf
import time
import scale
from prettytable import PrettyTable
import setting
import statistics
import csv



#NOTE:
	
input1 = sys.argv[1]
input2 = sys.argv[2]
input3 = sys.argv[3]



example=[]
running_directory = os.getcwd()


#For Automatic Transmission (AT)
# example.append(['AT AT1','runlim -s 6144 -r 3600 dnnf ../property/AT/property_11.py --network N ../network/AT/AT_NN-1.onnx  --save-violation violation'])

example.append([input1, 'runlim -s 6144 -r 3600 dnnf ..{} --network N ..{}  --save-violation violation'.format(input2,input3)])


csv_fields = ['Models', 'Property name','Simulation time','Surrogate model building time','#Experiments', '#Refinements', '#Simulations', 'Median', 'Falsifying time','Validation time', 'Total time', 'Inputs']
filename = "NNFal.csv"
csvFile = open(filename, 'w')
csvwriter = csv.writer(csvFile)
csvwriter.writerow(csv_fields)
N = 1 #Number of Experiments.
for i in range(0,len(example)):
	Number_verified = 0
	total_xspeed_time = 0
	total_overall_time = 0
	total_dnnf_time = 0
	total_num_simu = 0
	total_dx_time = 0
	Median_data = []
	print('\nrunning '+ example[i][0])
	
	for how_many in range(N):
		print(how_many+1)
		start_time = time.time()
		dnnf_cmd = example[i][1]
		refine_counter = 0
		refine_time = 0
		dnnf_time = 0
		while(True):
			os.chdir(running_directory)
			output = str(subprocess.run(dnnf_cmd, capture_output=True, shell=True))
			status = output.find("result: sat")
			status_memory = output.find("out of memory")
			status_time = output.find("out of time")
			if(status == -1):
				if(refine_counter != 0):
					dnnf.setInitialProperty(dnnf_cmd)
				if(status_memory != -1):
					print("Can't find a CE due to OOM.")
				if(status_time != -1):
					print("Can't find a CE due to Timeout.")
				break;
			else:
				print("Found a CE input.")
				res = " result:"
				res_str = output.find(res)
				res_start = int(res_str)+len(res)+0
				res_end = int(res_str)+len(res)+4
				result = output[res_start:res_end];
				
				res2 = "falsification time:"
				res2_str = output.find(res2)
				res2_start = int(res2_str)+len(res2)+0
				res2_end = int(res2_str)+len(res2)+16
				result2 = output[res2_start:res2_end];
				d_time = re.sub("[^\d\.]", "", result2)
				#print(example[i][0] +" is falisifyied with status ("+ result + " ) in time "+ d_time + " by DNNF.")
				#dnnf returns the Input and stored it into the list inputs as per the dimension.
				Input = np.load("violation.npy")
				#print(Input.tolist()[0])
				inputs = Input.tolist()[0]
				os.remove("violation.npy")

				#print(scale.data[example[i][0].split()[0]]['ST'])
				x_time = time.time()
				isReach, csvInputs =setting.common(inputs,example[i][0])
				#print(csvInputs)
				if (isReach):
					print("Found a trajectory after", refine_counter, "refinement in", (time.time() - x_time))
					xspeed_time = time.time() - x_time
					overall_time = time.time() - start_time
					total_xspeed_time += xspeed_time
					total_overall_time += overall_time
					total_dnnf_time += dnnf_time + float(d_time) + refine_time
					total_dx_time = total_dnnf_time + total_xspeed_time
					total_num_simu += refine_counter +1 
					Median_data.append(refine_counter +1)
					#print("Total time spend to falsify is", overall_time)
					#pt.add_row(["",how_many+1,refine_counter,dnnf_time+float(d_time),refine_time,xspeed_time,(dnnf_time+float(d_time)+refine_time + xspeed_time),overall_time])
					csvwriter.writerow([example[i][0].split()[0],example[i][0].split()[1],'','',how_many+1,refine_counter, refine_counter+1,'', dnnf_time+float(d_time),xspeed_time,(dnnf_time+float(d_time)+refine_time + xspeed_time), csvInputs])
					Number_verified = Number_verified + 1
					os.chdir(running_directory)
					if(refine_counter != 0):
						dnnf.setInitialProperty(dnnf_cmd)
					break;
				else:
					print("MATLAB Can't find a trajectory in", (time.time() - x_time), "time, refineing the property and run again...")
					os.chdir(running_directory)
					refine_counter = refine_counter + 1
					r_time = time.time()
					dnnf.refined_property(Input.tolist()[0],dnnf_cmd,refine_counter)
					refine_time += (time.time() - r_time)
					#print("Refine time is: ", (time.time() - r_time))
					dnnf_time += float(d_time) 
					
		x=time.time()
		dnnf.reset()
		if (how_many == N-1 and  Number_verified > 0):
			#pt.add_row([example[i][0], Number_verified, "Average time", total_dnnf_time/Number_verified,"", total_xspeed_time/Number_verified, total_dx_time/Number_verified, total_overall_time/Number_verified])
			csvwriter.writerow([example[i][0].split()[0], example[i][0].split()[1],scale.data[example[i][0].split()[0]]['ST'][0],scale.data[example[i][0].split()[0]]['TT'][0], Number_verified, "Average time", total_num_simu/Number_verified,statistics.median(Median_data), total_dnnf_time/Number_verified, total_xspeed_time/Number_verified, total_dx_time/Number_verified, '  Average scenario'])
			csvwriter.writerow(['', '','','', '', '', '','', '', '', '', ''])

	print("Number of instances verified by MATLAB is ",Number_verified,"out of",N)
