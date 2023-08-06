import os
import subprocess
import re

#XSpeed-plan must be installed in this directory.


def simulate(inputs,sys_variable,xspeed_cmd):
	os.chdir("..")
	os.chdir(str(os.getcwd()) + "/validation/XSpeed-plan/build")
	cmd = []
	sys_variable = list(sys_variable.split(" "))
	x_cmd = ' --initial "' 
	for index,var in enumerate(sys_variable):
		if(index == len(sys_variable)-1):
			x_cmd += "1*" + str(var) + " == " + str(inputs[index])
		else:
			x_cmd += "1*" + str(var) + " == " + str(inputs[index]) + " & "
	x_cmd += '"'
	xspeed_cmd += x_cmd
	output1 = str(subprocess.run(xspeed_cmd, capture_output=True, shell=True))

	violated = "Is violated trajectory found:"
	vio_traj = output1.find(violated)
	vio_traj_start = int(vio_traj)+len(violated)+0
	vio_traj_end = int(vio_traj)+len(violated)+16
	vio_traj = output1[vio_traj_start:vio_traj_end];
	vio_traj = re.sub("[^\d\.]", "", vio_traj)

	if (int(vio_traj) > 0):
		return True
	else:
		return False
