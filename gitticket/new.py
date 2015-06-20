import gitticket as gt
import tempfile
import os
import yaml
from hashlib import sha256

def get_from_temp(message):
	with tempfile.NamedTemporaryFile() as msg:
		msg.write(gt.commit_msg)
		msg.seek(0)
		os.system("vim {}".format(msg.name))
		msg.seek(0)
		return yaml.load(msg)
	

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
	class NoTitle     (Exception): pass
	class InvalidType (Exception): pass
	class InvalidState(Exception): pass
	class Duplicate   (Exception): pass

	try:
		#Quick new feature
		try:
			type_name = gt.subject[0]
			if type_name not in gt.branch_types: raise InvalidType(type_name)
			gt.commit_msg = '\n'.join( ''.join([s,type_name]) if 'type' in s else s for s in gt.commit_msg.split('\n'))
		except InvalidType as e:
			raise e
		except IndexError:
			pass
			
		info = get_from_temp(gt.commit_msg)
	
		#defaults
		if info['state'] is None:
			info['state'] = 'open'


		#Error checking
		if info['title'] is None: raise NoTitle
		if info['type' ] not in {'feature', 'hotfix', 'release', 'support'}:          raise InvalidType (info['type'])
		if info['state'] not in {'open', 'closed', 'in-progress', 'invalid', 'hold'}: raise InvalidState(info['state'])

		#Hash
		info['hash'] = sha256(info['title']).hexdigest()

		#Load current tickets from file
		ticks = gt.get_tickets()

		for i,t in enumerate(ticks):
			if t['hash'] == info['hash']:
				raise Duplicate(str(i))

		ticks.append(info)

		#Save the file to tickets directory
		gt.write_tickets(ticks)

		gt.repo.index.add(['.ticket'])
		gt.repo.index.commit('Added [{}-{}]'.format(gt.project(), info['hash'][:6]))
		gt.push()

		#show the ticket
		gt.print_ticket_header()
		gt.print_ticket(info)

	except NoTitle:           print "No title in commit. Aborting."
	except InvalidState as e: print "State not valid: {}"        .format(e)
	except InvalidType  as e: print "Type not valid: {}"         .format(e)
	except Duplicate    as e: print "Ticket already exists as {}".format(e)
