import gitticket as gt

def project():
	if gt.subject[0] == None:
		print 'git project <project-name>'
	#Check for project branch
	#Write the project to .git/current_project
	gt.open_in_dir('.git/current_project','w').write(gt.subject[0].upper())
