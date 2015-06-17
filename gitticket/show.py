import gitticket as gt
import re

def show():
	tickets = gt.get_tickets()
	try:
		if not gt.subject: raise Exception
		ticks_to_print = [gt.get_ticket(tickets, sub) for sub in gt.subject]
		gt.print_ticket_header()
		for ticket in ticks_to_print: gt.print_ticket(ticket)
	except:
		#show current ticket
		try:
			branch_name = gt.active_repo.active_branch.name
			match = re.search(r'\w+/\w+-(\w+)', branch_name)
			ticket = gt.get_ticket(tickets, match.group(1))
			gt.print_ticket_header()
			gt.print_ticket(ticket)
		except:
			print 'Not on a ticket branch'
