import gitticket as gt

def modify(state):
	tickets = gt.get_tickets()
	ticket  = gt.get_ticket(tickets, state)

	gt.mark_state(ticket, state, tickets)
	gt.commit('Marked [{}] as {}'.format(ticket['hash'][:6], state))
	gt.push()
