import gitticket as gt

def modify(state):
	try:
		tickets = gt.get_tickets()
		ticket  = gt.get_ticket(tickets, gt.subject[0])

		gt.mark_state(ticket, state, tickets)
		gt.commit('Marked [{}] as {}'.format(ticket['hash'][:6], state))
		gt.push()

	except gt.NoId:          print "No ticket id given"
	except gt.NoTicket as e: print "Ticket could not be found for: {}".format(e)
