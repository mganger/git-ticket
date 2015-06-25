
import run as sp
from contextlib import contextmanager
import os
join = os.path.join
ls = os.listdir
realpath = os.path.realpath

def get_top_level(path='.'):
	real = realpath(path)
	if '.git' in ls(real):
		return real
	up_one = realpath(join(real,'..'))
	if up_one == real:
		raise RuntimeError("Is this a valid Git Repository?")
	else:
		return get_top_level(up_one)

@contextmanager
def cd(newdir):
	prevdir = os.getcwd()
	os.chdir(os.path.expanduser(newdir))
	try:
		yield
	finally:
		os.chdir(prevdir)

class Repo:
	def __init__(self,directory='.'):
		self.working_tree_dir = get_top_level(directory)
		self.git_dir          = join(self.working_tree_dir,'.git')
		self.active_branch    = sp.check_output(['git','-C',self.working_tree_dir,'status']).split('\n')[0].split()[2]

	def clone(self,new_dir,branch=None):
		command = ['git','clone']
		if branch:
			command += ['-b', branch]
		command += [self.directory,new_dir]
		if not os.path.exists(new_dir):
			os.mkdir(new_dir)
		with cd(new_dir):
			sp.check_call(command)
		return Repo(new_dir)

	def pull(self):
		sp.check_call(['git','-C',self.directory,'pull'])

	def push(self):
		sp.check_call(['git','-C',self.directory,'push'])

	def add(self, file_name):
		sp.check_call(['git','-C',self.directory,'add']+[file_name])

	def commit(self,message):
		sp.check_call(['git','-C',self.directory,'commit','-m "',message,'"'])

	def checkout(self, branch):
		sp.check_call(['git','-C',self.directory,'checkout',branch])
