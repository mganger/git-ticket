
import gitticket as gt
import subprocess
import os

def start():
	try:
		#Check for ticket
		tickets = gt.get_tickets()
		ticket  = gt.get_ticket(tickets,gt.subject[0])

		#Check to see if we want to stash changes and pop them later
		stashed = None
		try:
			stashed = gt.verb[0]
			subprocess.check_call(['git','stash','save'])
		except: pass


		#Create a new branch like: git-flow feature start PROJECT-HASH-title-in-lowercase
		short_hash = str(ticket['hash'][:6])
		type_name  = str(ticket['type'])
		title      = re.sub(r'\s+','-',str(ticket['title']).lower())


		#set current ticket to in-progress
		gt.mark_state(ticket, 'in-progress', tickets)
		gt.commit('Started branch for [{}]'.format(ticket['hash'][:6]))
		gt.push()

		os.system("git flow {} start {}-{}-{}".format(type_name,gt.project(),short_hash,title))

		if stashed: subprocess.check_call(['git','stash','pop'])
	except:
		print "Cannot start ticket branch. If there are current changes, you may want to stash them first (or run git ticket start 3 stash)"

def finish():
	tickets = gt.get_tickets()
	ticket  = gt.get_ticket(tickets,gt.subject[0])

	short_hash = str(ticket['hash'][:6])
	type_name  = str(ticket['type'])
	title      = re.sub(r'\s+','-',str(ticket['title']).lower())

	#mark ticket as closed
	gt.mark_state(ticket, 'closed', tickets)
	gt.commit('Finished branch for [{}]'.format(ticket['hash'][:6]))
	gt.push()

	os.system("git flow {} finish {}-{}-{}".format(type_name,gt.project(),short_hash,title))
