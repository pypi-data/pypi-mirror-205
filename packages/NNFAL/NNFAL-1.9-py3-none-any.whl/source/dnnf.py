base_premises = "x_min <= x <= x_max"
temp_property = ""

def reset():
	global temp_property
	temp_property = ""


def refined_property(inputs,dnnf_cmd,refine_counter):
	global temp_property

	ref_property = "And("+ base_premises + ", Or( "
	for i in range(len(inputs)-1):
		if(i == len(inputs)-2):
			ref_property += "x[(0," + str(i) + ")] != "+ str(inputs[i])
		else:
			ref_property += "x[(0," + str(i) + ")] != "+ str(inputs[i]) + ", "
	ref_property += "))"
	if(refine_counter == 1):
		temp_property += ref_property
	else: 
		temp_property =temp_property.replace(base_premises,ref_property)
	
	prop_path = dnnf_cmd.split()[6]
	prop_file = open(prop_path,"r")
	data = prop_file.read()
	data = data.replace(base_premises,ref_property)
	prop_file.close()
	prop_file = open(prop_path, "w")
	prop_file.write(data)
	prop_file.close()


def setInitialProperty(dnnf_cmd):
	
	global temp_property
	
	prop_path = dnnf_cmd.split()[6]
	prop_file = open(prop_path,"r")
	data = prop_file.read()
	data = data.replace(temp_property,base_premises)
	prop_file.close()
	prop_file = open(prop_path, "w")
	prop_file.write(data)
	prop_file.close()
