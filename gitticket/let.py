import gitticket as gt

def let():
	class TwoTypes(Exception): pass
	class NoType  (Exception): pass

	try:
		verbs = set(gt.verb)
		relation = {'need','block'} & verbs

		if len(relation) > 1: raise TwoTypes
		if len(relation) < 1: raise NoType

		relation = relation.pop()
		print relation


		first_set  = {gt.subject[0]}
		second_set = {gt.subject[1]}

		if relation is 'block':
			gt.set_dependency(second_set, first_set)
		if relation is 'need':
			gt.set_dependency(first_set,  second_set)
			
	except gt.NoId:
		print "Missing ticket id"
	except gt.NoTicket as e:
		print "Invalid ticket: {}".format(e)
	except TwoTypes:
		print "Can't assign both a need and want relationship in the same command"
	except NoType:
		print "Need a relationship between tickets (need or block)"
	except gt.Circular:
		print "Circular dependency: {}"
