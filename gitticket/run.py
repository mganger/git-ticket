import os

def check_call(command_list):
	return os.system( ' '.join( str(x) for x in command_list )+' > /dev/null'  )

def check_output(command_list):
	return os.popen ( ' '.join( str(x) for x in command_list ) ).read()
