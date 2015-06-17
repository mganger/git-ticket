
import gitticket as gt

def show_list():
	subs = gt.subject
	allowed = subs[:1] if len(subs) == 1 else subs if subs and set(gt.verb) == {'and'} else ['open', 'in-progress']

	gt.print_ticket_header()

	for i,tick in enumerate(gt.get_tickets()):
		if tick['state'] in allowed or 'all' in allowed:
			gt.print_ticket(tick,i)

	#Make a tree of all open tickets
	#Make this deplist
	#	Show the hash as well as the number
	#all:
	#	show all tickets (open, closed, invalid, hold, in-progress)
	#open:
	#closed:
	#invalid:
	#in-progress
