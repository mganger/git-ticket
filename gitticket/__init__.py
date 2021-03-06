#This is the main interface to the package

import os
from gitrepo import Repo
active_repo = Repo(os.getcwd())

def init():
	import init
	init.init()
def show_list():
	import lister
	lister.show_list()
def show():
	import show
	show.show()
def start():
	import start
	start.start()
def finish():
	import start
	start.finish()
def modify(command):
	import state
	state.modify(command)
def new():
	import new
	new.new()
def proj():
	import project
	project.project()
	
def let():
	import let
	let.let()


import sys
args = sys.argv[1:]
#might want to change in the future
exit = sys.exit

#Structure of a git ticket statement:
#
#    git ticket let <id> need <id>
#    ---------- --- ---- ---- ----
#      subject  verb s   v    s
#
# - git ticket is obviously an implicit subject
# - the first verb is the command
# - if the command warrants it, you can chain alternating subjects and verbs

command = None
subject = None
verb    = None

try:
	command = args[0]
	subject = args[1::2]
	verb    = args[2::2]
except: pass

current_branch = active_repo.active_branch

def project():
	try:
		with open('.git/current_project') as file:
			return file.read().strip()
	except:
		print 'Project not initialized'

def project_branch():
	return 'ticket-'+project()


repo = None
try:
	import tempfile
	from hashlib import sha256
	temp_dir = tempfile.gettempdir()
	cloning_dir = os.path.join(temp_dir,sha256(project_branch()+active_repo.git_dir).hexdigest())
	if os.path.exists(cloning_dir):
		#If the repo exists, we assume that it is kept up to date by anything that modifies it
		repo = Repo(cloning_dir)
	else:
		repo = active_repo.clone(cloning_dir, branch=project_branch())
except Exception as e: print e

branch_types = {'feature', 'support', 'hotfix'}


commit_msg=\
"""title:      
type:       
assignee:   
start-date: 
due-date:   
state:      
comments:   
"""


join = os.path.join
def open_in_dir(filename, args = 'r'):
	return open(join(repo.working_tree_dir,filename), args)

def add_index(i,tick):
	tick['index'] = i
	return tick

import json
def get_tickets():
	with open_in_dir('.ticket') as file:
		return [ add_index(i,tick) for i, tick in enumerate(json.load(file)) ]
def write_tickets(obj):
	with open_in_dir('.ticket','w') as file:
		json.dump(obj,file, sort_keys=True, indent=2, separators=(',', ': '))
def add_file(*names):
	repo.add(*names)
def commit(string):
	repo.commit(string)
def get_index(tickets, ticket):
	for i,t in enumerate(tickets):
		if ticket['hash'] == t['hash']:
			return i


class NoId    (Exception): pass
class NoTicket(Exception): pass

def get_ticket(tickets,string):
	if string == 'Other': return {'title':'Other', 'hash':'0000000000', 'index': ''}
	try:
		#try to find by id
		if not string or string == '': raise NoId
		return tickets[int(string)]

	except (IndexError, ValueError):
		#try to find it by hash
		for tick in tickets:
			if string in tick['hash']:
				return tick
		raise NoTicket

def print_ticket(ticket,id=None):
	print_ticket_fields(
		id       = id if id else get_index(get_tickets(),ticket),
		hash     = ticket['hash'],
		state    = ticket['state'],
		assignee = ticket['assignee'],
		due      = ticket['due-date'],
		title    = ticket['title']
	)

def print_ticket_fields(id, hash, state, assignee, due, title):
	print "{:<8} {:<10} {:<15} {:<15} {:<15}  {}".format(
		id,
		hash[:6],
		state,
		assignee,
		due,
		title
	)

def print_ticket_header():
	print_ticket_fields('id','hash','state','assignee','due-date','title')
	print "-"*75

def print_ticket_list(tickets):
	pass


def mark_state(ticket, state, tickets):
	index = tickets.index(ticket)
	tickets[index]['state'] = state
	write_tickets(tickets)
	add_file('.ticket')


def checkout(name,this_repo=repo):
	b_current = this_repo.active_branch
	repo.checkout(name)
	return b_current

def push():
	repo.push()

def to_tuples(l):
	return [(a,b) for a,b in l]

def uniq(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]

class Circular(Exception): pass
def check_circle(old_deps, new_dep):
	first = new_dep[0]
	deps = old_deps + [new_dep]
	path = []

	try:
		current = first
		while True:
			next_dep = [ b for a,b in deps if a == current ][0]
			if next_dep in path:
				raise Circular
			path += [next_dep]
			current = next_dep

	except IndexError:
		pass

def get_dep_list():
	with open_in_dir('.dependencies') as f:
		return to_tuples(json.load(f))
	

def set_dependency(dependent, dependency):
	mapped = (dependent['hash'], dependency['hash'])
	try:
		deps = get_dep_list()
		check_circle(deps,mapped)
		with open_in_dir('.dependencies','w') as f:
			json.dump(uniq(deps+[mapped]),f, sort_keys=True, indent=2, separators=(',',': '))
	except IOError:
		with open_in_dir('.dependencies','w') as f:
			json.dump([],f,sort_keys=True, indent=2, separators=(',', ': '))
		set_dependency(dependent,dependency)

def remove_dependency(dependent, dependency):
	mapped = (dependent['hash'], dependency['hash'])
	try:
		deps = get_dep_list()
		with open_in_dir('.dependencies','w') as f:
			json.dump([t for t in deps if t != mapped],f, sort_keys=True, indent=2, separators=(',',': '))
	except IOError:
		print 'Could not write to file'

def dep_tree(l):
	from collections import defaultdict
	trees = defaultdict(dict)
	for parent, child in l:
		trees[parent][child] = trees[child]
	parents, children = zip(*l)
	roots = set(parents) - set(children)

	return {root: trees[root] for root in roots}
