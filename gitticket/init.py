import gitticket as gt
import os
import subprocess
import json

def init():

	#Create new branch with name ticket-PROJECT
	project = None
	try:
		project = gt.subject[0].upper()
	except:
		print 'git-ticket init <project-name>'
		exit(0)

	#SHA is empty commit
	#TODO assert project doesn't already exist
	with open(os.devnull, 'wb') as devnull:
		try:
			past_branch = gt.current_branch

			subprocess.check_call(['git', 'checkout', '--orphan', 'ticket-{}'.format(project)],stdout=devnull,stderr=subprocess.STDOUT)
			os.system("git clean -fdx")
			os.system("git reset")
			with open(project, 'w') as file:
				file.write(project+'\n')

			with open('.ticket', 'w') as file:
				json.dump([],file)

			os.system("git add .ticket {}".format(project));
			os.system('git commit -m "Initial commit of ticket-{} branch"'.format(project))
			with open('.git/current_project', 'w') as file:
				file.write(project)

			print "Initialized project {}".format(project)

		except:
			print "Couldn't initialize branch. Does it already exist?"
		finally:
			try: subprocess.check_call("git checkout {} --force".format(past_branch).split(), stdout=devnull)
			except: pass
			#TODO add commit hook to folder (.git/hooks/commit-msg)
			gt.exit(0)
