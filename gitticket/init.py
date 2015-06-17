import gitticket as gt
import os
import subprocess
import json

def init():
	#Use project name
	assert gt.subject[0] != '', 'git-ticket init <project-name>'

	#Create new branch with name ticket-PROJECT
	project = gt.subject[0].upper()

	#SHA is empty commit
	#TODO assert project doesn't already exist
	with open(os.devnull, 'wb') as devnull:
		try:
			past_branch = gt.current_branch

			subprocess.check_call(["git checkout --orphan ticket-{}"].format(project),stdout=devnull,stderr=subprocess.STDOUT)
			os.system("git clean -fdx")
			os.system("git reset")

			open(project, 'w').write(project+'\n').close()
			with open('.ticket', 'w') as file:
				json.dump([],file)

			os.system("git add {} .ticket".format(project))
			os.system('git commit -m "Inital commit of ticket-{} branch"'.format(project))
			os.system('git-ticket project {}'.format(project))

			print "Initialized project {}".format(project)

		except:
			print "Couldn't initialize branch. Does it already exist?"
		finally:
			try: subprocess.check_call(["git checkout {}".format(past_branch)], stdout=devnull)
			except: pass
			#TODO add commit hook to folder (.git/hooks/commit-msg)
			gt.exit(0)
