import os
import subprocess
import re
import numpy as np
import xspeed
import dnnf
import time
import scale
from prettytable import PrettyTable

#NOTE: We have to change the model file in validation loop.
	



example=[]
running_directory = os.getcwd()

#example = ['Networks and property', 'Dimensions as per validation engine', 'dnnf_cmd', 'XSpeed_cmd']


#For Oscillator instances...

#example.append(['Oscillator_NN P1', 'p q', 'runlim -s 8192 -r 3600 dnnf ../property/Oscillator/property_11.py --network N ../network/Oscillator/Osc_NN-1.onnx --save-violation violation','./XSpeed-plan  -m ../benchmarks/NNFal/Oscillator.xml -c ../benchmarks/NNFal/Oscillator.cfg --depth 7 --time-step 0.001 --time-horizon 10 -o out.txt -v p,q -F "loc=-1 & 1*p<=0.193 & 1*p>=0.1 & 1*q<=-0.25 & 1*q>=-0.3" -e validation'])


#example.append(['Oscillator_NN P2', 'p q', 'runlim -s 8192 -r 3600 dnnf ../property/Oscillator/property_22.py --network N ../network/Oscillator/Osc_NN-1.onnx --save-violation violation','./XSpeed-plan  -m ../benchmarks/NNFal/Oscillator.xml -c ../benchmarks/NNFal/Oscillator.cfg --depth 7 --time-step 0.001 --time-horizon 100 -o out.txt -v p,q -F "loc=-1 & 1*p<=-0.45029 & 1*p>=-0.5 & 1*q<=0.1968 & 1*q>=0.1" -e validation'])


#example.append(['Oscillator_NN P3', 'p q', 'runlim -s 8192 -r 3600 dnnf ../property/Oscillator/property_33.py --network N ../network/Oscillator/Osc_NN-1.onnx --save-violation violation','./XSpeed-plan  -m ../benchmarks/NNFal/Oscillator.xml -c ../benchmarks/NNFal/Oscillator.cfg --depth 7 --time-step 0.001 --time-horizon 100 -o out.txt -v p,q -F "loc=-1 & 1*p<=0.1 & 1*p>=0 & 1*q<=0.15 & 1*q>=0.13485" -e validation'])



#For Two tanks instances...

#example.append(['Two_tanks_NN P1', 'x1 x2', 'runlim -s 8192 -r 3600 dnnf ../property/Two_tanks/property_11.py --network N ../network/Two_tanks/Two_tanks_NN-1.onnx --save-violation violation','./XSpeed-plan -m ../benchmarks/NNFal/two_tanks.xml -c ../benchmarks/NNFal/two_tanks.cfg --time-horizon 50 --time-step 0.01 --depth 10 -o out.txt -v x1,x2 -F "loc=-1 & 1*x1 >= 1 & 1*x1 <= 1.5 & 1*x2 >=-0.4 & 1*x2<= -0.23" -e validation'])


example.append(['Two_tanks_NN P2','x1 x2', 'runlim -s 8192 -r 3600 dnnf ../property/Two_tanks/property_22.py --network N ../network/Two_tanks/Two_tanks_NN-1.onnx --save-violation violation','./XSpeed-plan -m ../benchmarks/NNFal/two_tanks.xml -c ../benchmarks/NNFal/two_tanks.cfg --time-horizon 50 --time-step 0.01 --depth 10 -o out.txt -v x1,x2 -F "loc=-1 & 1*x1 >= 0 & 1*x1 <= 0.10 & 1*x2 >=-0.215 & 1*x2<= -0.200" -e validation'])


#example.append(['Two_tanks_NN P3','x1 x2', 'runlim -s 8192 -r 3600 dnnf ../property/Two_tanks/property_33.py --network N ../network/Two_tanks/Two_tanks_NN-1.onnx --save-violation violation','./XSpeed-plan -m ../benchmarks/NNFal/two_tanks.xml -c ../benchmarks/NNFal/two_tanks.cfg --time-horizon 50 --time-step 0.01 --depth 10 -o out.txt -v x1,x2 -F "loc=-1 & 1*x1 >= 0 & 1*x1 <= 0.40 & 1*x2 >=-0.500 & 1*x2<= -0.465" -e validation'])


#example.append(['Two_tanks_NN P4','x1 x2', 'runlim -s 8192 -r 3600 dnnf ../property/Two_tanks/property_44.py --network N ../network/Two_tanks/Two_tanks_NN-1.onnx --save-violation violation','./XSpeed-plan -m ../benchmarks/NNFal/two_tanks.xml -c ../benchmarks/NNFal/two_tanks.cfg --time-horizon 50 --time-step 0.001 --depth 10 -o out.txt -v x1,x2 -F "loc=-1 & 1*x1 >= -0.20 & 1*x1 <= 0.20 & 1*x2 >= 0.30 & 1*x2<= 0.35" -e validation'])


#example.append(['Two_tanks_NN P5','x1 x2', 'runlim -s 8192 -r 3600 dnnf ../property/Two_tanks/property_55.py --network N ../network/Two_tanks/Two_tanks_NN-1.onnx --save-violation violation','./XSpeed-plan -m ../benchmarks/NNFal/two_tanks.xml -c ../benchmarks/NNFal/two_tanks.cfg --time-horizon 50 --time-step 0.001 --depth 10 -o out.txt -v x1,x2 -F "loc=-1 & 1*x1 >= -0.20 & 1*x1 <= 0.20 & 1*x2 >= 0.31 & 1*x2<= 0.35" -e validation'])




#For NAV_30 instances...

#example.append(['NAV_30_NN P1', 'x1 x2 v1 v2', 'runlim -s 8192 -r 3600 dnnf ../property/NAV/NAV_30/property_11.py --network N ../network/NAV/NAV_30/NAV_30_NN-1.onnx --save-violation violation','./XSpeed-plan -m ../benchmarks/NNFal/30.xml -c ../benchmarks/NNFal/30.cfg --time-horizon 50 --time-step 0.001 --depth 100 -o out.txt -v x1,x2 -F "loc=298 & 1*x1>=22 & 1*x1<=23 & 1*x2>=11 & 1*x2<=12" -e validation'])


#example.append(['NAV_30_NN P2', 'x1 x2 v1 v2', 'runlim -s 8192 -r 3600 dnnf ../property/NAV/NAV_30/property_22.py --network N ../network/NAV/NAV_30/NAV_30_NN-1.onnx --save-violation violation','./XSpeed-plan -m ../benchmarks/NNFal/30.xml -c ../benchmarks/NNFal/30.cfg --time-horizon 50 --time-step 0.01 --depth 100 -o out.txt -v x1,x2 -F "loc=412 & 1*x1>=11 & 1*x1<=12 & 1*x2>=16 & 1*x2<=17" -e validation'])


#example.append(['NAV_30_NN P3', 'x1 x2 v1 v2', 'runlim -s 8192 -r 3600 dnnf ../property/NAV/NAV_30/property_33.py --network N ../network/NAV/NAV_30/NAV_30_NN-1.onnx --save-violation violation','./XSpeed-plan -m ../benchmarks/NNFal/30.xml -c ../benchmarks/NNFal/30.cfg --time-horizon 50 --time-step 0.001 --depth 100 -o out.txt -v x1,x2 -F "loc=233 & 1*x1>=7 & 1*x1<=8 & 1*x2>=9 & 1*x2<=10" -e validation'])



#For Bouncing ball instance...

#example.append(['B_ball_NN P1','x v', 'runlim -s 8192 -r 3600 dnnf ../property/Bball/property_11.py --network N ../network/Bball/Bball_NN-1.onnx --save-violation violation ','./XSpeed-plan -m ../benchmarks/NNFal/bball.xml -c ../benchmarks/NNFal/bball.cfg --time-horizon 10 --time-step 0.001 --depth 30 -o out.txt -v x,v -F "loc=-1 & 1*v >= 11.10" -e validation'])



#For Adaptive Cruise Controller instances...
#example.append(['ACCU04_NN P1', 'x0 x1 x2 x3 c1 c2 c3 aut1_d01 aut2_d01 aut3_d01', 'runlim -s 8192 -r 3600 dnnf ../property/ACCU/property_11.py --network N ../network/ACCU/ACCU04_NN-1.onnx --save-violation violation', './XSpeed-plan -m ../benchmarks/NNFal/ACCU04.xml -c ../benchmarks/NNFal/ACCU04.cfg --time-horizon 10 --time-step 0.5 --depth 10 -o out.txt -v x0,x1 -F "loc=19|20|21|22|23|24|25|26|27|7|8|9|16|17|18|3|6|12|15" -e validation'])


table_fields = ['Property name','#Experiments', '#Refinements', 'DNNF_Time', 'Refine_Time','XSpeed_Time', 'D+X_Time', 'Overall_time']
pt = PrettyTable(table_fields)
pt.title = "NNFal instances"
N = 10 #Number of Experiments.
for i in range(0,len(example)):
	Number_verified = 0
	total_xspeed_time = 0
	total_overall_time = 0
	total_dnnf_time = 0
	total_dx_time = 0
	print('\nrunning '+ example[i][0])
	pt.add_row([example[i][0],"","","","","","",""])
	for how_many in range(N):
		print(how_many+1)
		start_time = time.time()
		dnnf_cmd = example[i][2]
		xspeed_cmd = example[i][3]
		sys_variable = example[i][1]
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
					print("DNNF can't find CE due to OOM.")
				if(status_time != -1):
					print("DNNF can't find CE due to Timeout.")
				break;
			else:
				print("DNNF found a CE input.")
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
				#print(time.time() - start_time)
				print(example[i][0] +" is falisifyied with status ("+ result + " ) in time "+ d_time + " by DNNF.")
				#dnnf returns the Input and stored it into the list inputs as per the dimension.
				Input = np.load("violation.npy")
				print(Input.tolist()[0])
				
				#call XSpeed to find a trajectory from the returned inputs
		
				x_time = time.time()
				#isReach =  xspeed.simulate(scale.inv_scaling(Input.tolist()[0]),sys_variable,xspeed_cmd)
				isReach =  xspeed.simulate(scale.inv_scaling(Input.tolist()[0], example[i][0].split()[0]),sys_variable,xspeed_cmd)
				if (isReach):
					print("Found a trajectory after", refine_counter, "refinement in", (time.time() - x_time))
					xspeed_time = time.time() - x_time
					overall_time = time.time() - start_time
					total_xspeed_time += xspeed_time
					total_overall_time += overall_time
					total_dnnf_time += dnnf_time + float(d_time) + refine_time
					total_dx_time = total_dnnf_time + total_xspeed_time
					print("Total time spend to falsify by dnnf and verified by xspeed is", overall_time)
					pt.add_row(["",how_many+1,refine_counter,dnnf_time+float(d_time),refine_time,xspeed_time,(dnnf_time+float(d_time)+refine_time + xspeed_time),overall_time])
					Number_verified = Number_verified + 1
					os.chdir(running_directory)
					if(refine_counter != 0):
						dnnf.setInitialProperty(dnnf_cmd)
					break;
				else:
					print("XSpeed Can't find a trajectory in", (time.time() - x_time), "time, refineing the property and run again dnnf...")
					os.chdir(running_directory)
					refine_counter = refine_counter + 1
					r_time = time.time()
					dnnf.refined_property(Input.tolist()[0],dnnf_cmd,refine_counter)
					refine_time += (time.time() - r_time)
					#print("Refine time is: ", (time.time() - r_time))
					dnnf_time += float(d_time) 
					
		x=time.time()
		#print(x)
		dnnf.reset()
		#print(time.time()-x)
		if (how_many == N-1 and  Number_verified > 0):
			pt.add_row([example[i][0], Number_verified, "Average time", total_dnnf_time/Number_verified,"", total_xspeed_time/Number_verified, total_dx_time/Number_verified, total_overall_time/Number_verified])

	print("Number of instances verified by xspeed is ",Number_verified,"out of",N)
	pt.add_row(["","","","","","","",""])
	with open('xspeed_resul_timeout_2.txt', 'a') as f:
    		f.write(str(pt))
	f.close()
print(pt)


with open('xspeed_result_timeout_2_copy.txt', 'a') as f:
    f.write(str(pt))
