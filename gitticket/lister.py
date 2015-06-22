
import gitticket as gt

def print_dep_tree(tree, tickets, indent=0, prefix = ''):
	if tree == {}: return
	items = [ (gt.get_ticket(tickets,key),value) for key,value in tree.items() ]
	pruned = [ (t,v) for t,v in items if v != {} or t['state'] in {'open','in-progress'} ]
	last = None
	try: last = pruned[-1][0]
	except: pass
	for t,value in pruned:
		print '{i:<5} {prefix}{char}-- {title}'.format(
			i      = t['index'],
			prefix = prefix,
			char   = '`' if last == t else '|',
			title  = t['title'] )
		print_dep_tree(
			tree    = value,
			indent  = indent+1,
			tickets = tickets,
			prefix  = prefix + ('|   ' if t != last else '    ') )

def show_list():
	subs = gt.subject
	allowed = subs[:1] if len(subs) == 1 else subs if subs and set(gt.verb) == {'and'} else ['open', 'in-progress']


	try:
		if not gt.subject[0] in {'deps','depends','dependencies'}:
			raise Exception
		tickets = gt.get_tickets()
		dep_list = gt.get_dep_list()
		in_deps = [b for a in dep_list for b in a]
		dep_list += [('Other',a['hash']) for a in tickets if a['hash'] not in in_deps]
		print 'Dependency Tree:'
		print '--------------- '
		print_dep_tree(gt.dep_tree(dep_list), tickets=tickets)
	except Exception as e:
		gt.print_ticket_header()
		for i,tick in enumerate(gt.get_tickets()):
			if tick['state'] in allowed or 'all' in allowed:
				gt.print_ticket(tick,i)
