import gitticket as gt

def let():
	class TwoTypes(Exception): pass
	class NoType  (Exception): pass

	try:
		verbs = set(gt.verb)
		relation = {'need','block','release'} & verbs

		if len(relation) > 1: raise TwoTypes
		if len(relation) < 1: raise NoType

		relation = relation.pop()

		tickets    = gt.get_tickets()
		first_set  = gt.get_ticket(tickets, gt.subject[0])
		second_set = gt.get_ticket(tickets, gt.subject[1])

		if relation == 'block':
			gt.set_dependency(second_set, first_set)
		if relation == 'need':
			gt.set_dependency(first_set,  second_set)
		if relation == 'release':
			gt.remove_dependency(first_set, second_set)

		gt.repo.index.add   (['.dependencies'])
		gt.repo.index.commit( 'Added dependency: {} {}s {}'.format(first_set['hash'][:6],relation,second_set['hash'][:6]) )
		gt.push()
		print 'Added dependency' if relation != 'release' else 'Released dependency'
			
	except gt.NoId:
		print "Missing ticket id"
	except gt.NoTicket as e:
		print "Invalid ticket: {}".format(e)
	except TwoTypes:
		print "Can't assign both a need and want relationship in the same command"
	except NoType:
		print "Need a relationship between tickets (need, block, or release)"
	except gt.Circular as e:
		print "Circular dependency: {}".format(e)
	except OSError:
		print "Couldn't write dependencies to disk"
