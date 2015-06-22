import os

def check_call(command_list):
	return os.system( ' '.join(command_list)+' > /dev/null'  )

def check_output(command_list):
	return os.popen( ' '.join(command_list) ).read()
