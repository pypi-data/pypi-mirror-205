import time
from scale import inv_scaling
# import pytomatlab
import subprocess
import pandas as pd


def AT_set(inputs, prop):
    inputs_denormalized = inv_scaling(inputs, "AT")
    #print(inputs_denormalized)
    
    th0 = inputs_denormalized[3]
    br0 = inputs_denormalized[4]
    th1 = inputs_denormalized[5]
    br1 = inputs_denormalized[6]
    th2 = inputs_denormalized[7]
    br2 = inputs_denormalized[8]
    th3 = inputs_denormalized[9]
    br3 = inputs_denormalized[10]
    
    time_step = 5
    T = 30
    csvInputs = {}
    for i in range(0,len(inputs_denormalized),2):
        if (i*time_step < 30):
           csvInputs[i*time_step] = [inputs_denormalized[i+3],inputs_denormalized[i+4]]
           csvInputs[(i+1)*time_step] = [inputs_denormalized[i+3],inputs_denormalized[i+4]]
        if (i*time_step == 30):
           csvInputs[i*time_step] = [inputs_denormalized[i+3],inputs_denormalized[i+4]]


    matlab_cmd = f"python3 ../validation/matlab/AT/pytomatlab_AT.py {th0} {br0} {th1} {br1} {th2} {br2} {th3} {br3}"
    
    output_matlab = str(subprocess.run(matlab_cmd, capture_output=True, shell=True))
    
    #print(output_matlab)
    df1 = pd.read_csv('yout.csv', names=["v", "w", "g"])
    #print(df1)
    
    if (prop == "AT6c"):
        V = df1.loc[0:2000]
        W = df1.loc[0:3000]
        #print(df1.loc[0:2000]['v'])
        #print(df1.loc[0:3000]['w'])
        count=len(W[W['w'] >= 3000])
        count2 = len(V[V['v'] > 65])
        #print(count)
        #print(count2)
        if (count == 0):
           if (count2):
              return True, csvInputs
           else:
              return False, csvInputs
        else:
            return False, csvInputs
           
    elif(prop == "AT1"):
        df1 = df1.loc[0:2000]
        count = len(df1[df1['v'] >= 120])
        #print(count)
        if(count):
            return True, csvInputs
        else:
            return False, csvInputs
            

    
def AFC_P_set(inputs, prop):
    inputs_denormalized = inv_scaling(inputs, "AFC_P")
    #print(inputs_denormalized)
      
    th0 = inputs_denormalized[0]
    om0 = inputs_denormalized[1]
    th1 = inputs_denormalized[2]
    om1 = inputs_denormalized[3]
    th2 = inputs_denormalized[4]
    om2 = inputs_denormalized[5]
    th3 = inputs_denormalized[6]
    om3 = inputs_denormalized[7]
    th4 = inputs_denormalized[8]
    om4 = inputs_denormalized[9]
    th5 = inputs_denormalized[10]
    om5 = inputs_denormalized[11]
    
    time_step = 5
    T = 50
    csvInputs = {}
    for i in range(0,len(inputs_denormalized),2):
        if (i*time_step < 50):
           csvInputs[i*time_step] = [inputs_denormalized[i],inputs_denormalized[i+1]]
           csvInputs[(i+1)*time_step] = [inputs_denormalized[i],inputs_denormalized[i+1]]
        if (i*time_step == 50):
           csvInputs[i*time_step] = [inputs_denormalized[i],inputs_denormalized[i+1]]


    matlab_cmd = f"python3 ../validation/matlab/AFC_P/pytomatlab_AFC.py {th0} {om0} {th1} {om1} {th2} {om2} {th3} {om3} {th4} {om4} {th5} {om5}"
    
    output_matlab = str(subprocess.run(matlab_cmd, capture_output=True, shell=True))
    #print(output_matlab)
    
    df1 = pd.read_csv('yout.csv', names=["miu", "Mode"])
    #print(df1)
    count = len(df1[df1['miu'] > 0.007])
    #print(count)
    if(count):
        return True, csvInputs
    else:
        return False, csvInputs
        
        


def SC_set(inputs, prop):
    inputs_denormalized = inv_scaling(inputs, "SC")
    #print(inputs_denormalized)
    
    S0 = inputs_denormalized[0]
    S1 = inputs_denormalized[1]
    S2 = inputs_denormalized[2]
    S3 = inputs_denormalized[3]
    S4 = inputs_denormalized[4]
    S5 = inputs_denormalized[5]
    S6 = inputs_denormalized[6]
    S7 = inputs_denormalized[7]
    S8 = inputs_denormalized[8]
    S9 = inputs_denormalized[9]
    S10 = inputs_denormalized[10]
    S11 = inputs_denormalized[11]
    S12 = inputs_denormalized[12]
    S13 = inputs_denormalized[13]
    S14 = inputs_denormalized[14]
    S15 = inputs_denormalized[15]
    S16 = inputs_denormalized[16]
    S17 = inputs_denormalized[17]
    S18 = inputs_denormalized[18]
    S19 = inputs_denormalized[19]
    S20 = inputs_denormalized[20]
    time_step = 1.75
    T = 35
    csvInputs = {}
    for i,j in enumerate(inputs_denormalized):
         if (i*time_step <= T):
             csvInputs[i*time_step] = inputs_denormalized[i]

    matlab_cmd = f"python3 ../validation/matlab/SC/pytomatlab_SC.py {S0} {S1} {S2} {S3} {S4} {S5} {S6} {S7} {S8} {S9} {S10} {S11} {S12} {S13} {S14} {S15} {S16} {S17} {S18} {S19} {S20}"
    
    output_matlab = str(subprocess.run(matlab_cmd, capture_output=True, shell=True))
    
    #print(output_matlab)
    df1 = pd.read_csv('yout.csv', names=["A", "B", "C", "P"])
    #print(df1)
    count1 = len(df1[df1['P'] < 87])
    count2 = len(df1[df1['P'] > 87.5])
    #print(count1)
    #print(count2)
    if(count1 or count2):
       return True, csvInputs
    else: 
       return False, csvInputs



def CC_set_v1(inputs, prop):

    inputs_denormalized = (inv_scaling(inputs, "CC"))
    #print(inputs_denormalized)
    
    th0 = inputs_denormalized[0]
    br0 = inputs_denormalized[1]
    th1 = inputs_denormalized[2]
    br1 = inputs_denormalized[3]
    th2 = inputs_denormalized[4]
    br2 = inputs_denormalized[5]
    th3 = inputs_denormalized[6]
    br3 = inputs_denormalized[7]
    th4 = inputs_denormalized[8]
    br4 = inputs_denormalized[9]
    th5 = inputs_denormalized[10]
    br5 = inputs_denormalized[11]
    
    
    time_step = 5
    T = 100
    csvInputs = {}
    for i in range(0, len(inputs_denormalized), 2):
         if ((i+i)*time_step < 100):
             csvInputs[(i+i)*time_step] = [inputs_denormalized[i],inputs_denormalized[i+1]]
             csvInputs[((i+i)+1)*time_step] = [inputs_denormalized[i],inputs_denormalized[i+1]]
             csvInputs[((i+i)+2)*time_step] = [inputs_denormalized[i],inputs_denormalized[i+1]]
             csvInputs[((i+i)+3)*time_step] = [inputs_denormalized[i],inputs_denormalized[i+1]]
             
         if ((i+i)*time_step == T):
             csvInputs[(i+i)*time_step] = [inputs_denormalized[i],inputs_denormalized[i+1]]


    matlab_cmd = f"python3 ../validation/matlab/CC/pytomatlab_CC_inputs.py {th0} {br0} {th1} {br1} {th2} {br2} {th3} {br3} {th4} {br4} {th5} {br5}"

    output_matlab = str(subprocess.run(matlab_cmd, capture_output=True, shell=True))
    #print(output_matlab)
    df2=pd.DataFrame()
    df1 = pd.read_csv('yout.csv', names=["Car1", "Car2", "Car3","Car4","Car5"])
    df2['y5-y4']=df1['Car5'].sub(df1['Car4'],axis=0)
    #print(df2)
    count = len(df2[df2['y5-y4'] > 40])
    #print(count)
    if(count==0):
        return False, csvInputs
    else:
        return True, csvInputs


def F16_set(inputs):
    # call the inv_scaling function to denormalize the inputs list
    inputs_denormalized = inv_scaling(inputs, "F16")
    #print(inputs_denormalized)

    # call Matlab to find a trajectory from the returned inputs
    #matlab_time = time.time()
    phig = inputs_denormalized[3]
    thetag = inputs_denormalized[4]
    psig = inputs_denormalized[5]

    matlab_cmd = f"python3 ../validation/matlab/F_16/pytomatlab_F16.py {phig} {thetag} {psig}"
    # print(matlab_cmd)
    output_matlab = str(subprocess.run(matlab_cmd, capture_output=True, shell=True))
    # print(output_matlab)
    count = output_matlab.find("CRASHED")
    if(count==0):
        return False
    else:
        return True



def common(inputs,examples):
	example = examples.split()[0]
	prop = examples.split()[1]
		
	if(example.find("AT")>=0):
		#print("AT")
		output, csvInputs = AT_set(inputs, prop)
	elif(example.find("AFC_P")>=0):
		#print("AFC_P")
		output, csvInputs =AFC_P_set(inputs, prop)
	elif(example.find("SC")>=0):
		#print("SC")
		output, csvInputs =SC_set(inputs, prop)
	elif(example.find("CC")>=0):
		#print("CC_v1")
		output, csvInputs =CC_set_v1(inputs, prop)
	return output, csvInputs
