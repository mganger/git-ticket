
import subprocess as sp
from contextlib import contextmanager
import os

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
		self.directory = directory
		self.git_dir   = sp.check_output( 'git rev-parse --show-toplevel'.split() ).strip()
		self.working_tree_dir = directory
		self.active_branch = sp.check_output(['git','-C',self.directory,'status']).split('\n')[0].split()[2]

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

	def add(self, file_list):
		sp.check_call(['git','-C',self.directory,'add']+file_list)

	def commit(self,message):
		sp.check_call(['git','-C',self.directory,'commit','-m',message])

	def checkout(self, branch):
		sp.check_call(['git','-C',self.directory,'checkout',branch])
