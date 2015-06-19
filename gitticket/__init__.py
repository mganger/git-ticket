#This is the main interface to the package

from git import Repo
import os
active_repo = Repo(os.getcwd())

import init
import list
import start
import state
import show
import new
import project as proj
import let


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

current_branch = active_repo.active_branch.name

def project():
	try:
		with open('.git/current_project') as file:
			return file.read().strip()
	except:
		print 'Project not initialized'

def project_branch():
	return 'ticket-'+project()

import tempfile
cloning_dir = tempfile.mkdtemp()

repo = None
try:    repo = active_repo.clone(cloning_dir, b=project_branch())
except: pass

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

import json
def get_tickets():
	with open_in_dir('.ticket') as file:
		return json.load(file)
def write_tickets(obj):
	with open_in_dir('.ticket','w') as file:
		json.dump(obj,file, sort_keys=True, indent=2, separators=(',', ': '))
def add_file(*names):
	repo.index.add(names)
def commit(string):
	repo.index.commit(string)


class NoId    (Exception): pass
class NoTicket(Exception): pass

def get_ticket(tickets,string):
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
		id       = (id if id else get_tickets().index(ticket)),
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
	repo.git.checkout(name)
	return b_current

def push():
	repo.git.push()


class Circular(Exception): pass
def check_circle(deps, new_dep):
	first    = new_dep.key()
	current  = first
	all_deps = deps + new_dep
	path = []
	try:
		while True:
			next_dep = all_deps[current]
			if next_dep in path:
				raise Circular
			path += [next_dep]
	except KeyError:
		pass

def set_dependency(dependent, dependencies):
	try:
		#assume iterable
		for i in dependencies:
			set_dependency(dependent, i)
	except TypeError:
		#means that it wasn't iterable
		mapped = {dependent['hash']: dependencies['hash']}
		try:
			with open_in_dir('.dependencies') as file:
				deps = json.load(file)
				check_circle(deps,mapped)
			with open_in_dir('.dependencies','w') as file:
				json.dump(deps+mapped)
		except IOError:
			with open('.dependencies','w') as file:
				json.dump(file,[])
			set_dependency(dependent,dependencies)
