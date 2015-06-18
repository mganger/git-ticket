import gitticket as gt
import tempfile
import os
import yaml
from hashlib import sha256

def new():
	#Get a tmp file and do the whole git commit thing
	#Parse the ticket for (use yaml):
	#	title
	#	assignee       (default current)
	#	start-date     (default today)
	#	due-date       (optional)
	#	type           (default feature, else hotfix, support)
	#	state          (default open)
	#	comments
	info = []
	with tempfile.NamedTemporaryFile() as msg:
		msg.write(gt.commit_msg)
		msg.seek(0)
		os.system("vim {}".format(msg.name))
		msg.seek(0)
		info = yaml.safe_load(msg)
	#defaults
	if info['state'] is None:
		info['state'] = 'open'


	#Error checking
	if info['title'] is None:
		print 'Abort new ticket'
		exit(1)
	if info['type'] not in {'feature', 'hotfix', 'release', 'support'}:
		print 'Invalid type'
		exit(2)
	if info['state'] not in {'open', 'closed', 'in-progress', 'invalid', 'hold'}:
		print 'Invalid state'

	#Hash
	info['hash'] = sha256(info['title']).hexdigest()

	#Change branches

	#Load current tickets from file
	ticks = gt.get_tickets()

	for ticket in ticks:
		 if ticket['hash'] == info['hash']:
			print 'Ticket already exists'
			exit(1)

	ticks.append(info)

	#Save the file to tickets directory
	gt.write_tickets(ticks)

	gt.repo.index.add(['.ticket'])
	gt.repo.index.commit('Added [{}-{}]'.format(gt.project(), info['hash'][:6]))
	gt.push()

	#show the ticket
	gt.print_ticket_header()
	gt.print_ticket(info)
