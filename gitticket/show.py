import gitticket as gt
import re

def show():
	tickets = gt.get_tickets()
	try:
		if len(gt.subject) == 0: raise gt.NoId

		ticks_to_print = [gt.get_ticket(tickets, sub) for sub in gt.subject]

		gt.print_ticket_header()
		for ticket in ticks_to_print:
			gt.print_ticket(ticket)

	except gt.NoId:
		#show current ticket
		try:
			match  = re.search(r'\w+/\w+-(\w+)', gt.current_branch)
			ticket = gt.get_ticket(tickets, match.group(1))

			gt.print_ticket_header()
			gt.print_ticket(ticket)
		except AttributeError:
			print 'Not on a ticket branch (feature,hotfix,or support)'

	except gt.NoTicket as e:
		print 'Invalid ticket {}'.format(e)
