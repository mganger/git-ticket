Git-Ticket
==========

Git-ticket is intended to be a full-featured distributed ticketing system. It is
inspired in large part by ticgit-ng, and partially by Jira. It is not intended
to replace large scale ticketing systems; rather, it is intended to make feature
and bug tracking easy for small/medium sized projects. Additionaly, the
interface is written to be solely commandline, as there are already great
ticketing systems out there with nice web interfaces.

It is still under heavy development, so any feature is liable to break. If
something does break, you are encouraged to submit a ticket (and optionally fix
it yourself).

Dependencies
------------
git-flow
GitPython

Installation
------------

The easiest way to get dependencies is to use pip:

	sudo pip install gitpython

To install, just go to the root directory and run:

	sudo python setup.py install

Or if you would like to develop (installs a symlink to the current directory so
that changes can be observed instantly):

	sudo python setup.py develop

Then, in a git repo, run:

	git flow init
	git ticket init

Example Usage
-------------

### Creating

When creating a ticket, the title and the type are required. Valid types are
feature, hotfix, support, release.

Create a new ticket:

	git ticket new

Create a new ticket with type feature/hotfix/release/support:

	git ticket new feature
	git ticket new hotfix
	git ticket new release
	git ticket new support

### Listing
By default, it only lists tickets that are open or in-progress. You can override
this like below. Valid states are open, closed, in-progress, and invalid. Open
means it has not been addressed, closed means it has, in-progress means there is
a branch open for the ticket, and invalid means what you want (duplicate, not a
useful feature, etc.).

List tickets in repo:

	git ticket list
	git ticket list all
	git ticket list open
	git ticket list open and closed and invalid


### Developing
Start a git flow branch using ticket by id (the branch type corresponds to the
ticket type):

	git ticket start 34

Or by hash:

	git ticket start 64a9g2

Finish the branch (merging as necessary):

	git ticket finish 34

### Dependencies
You can add dependencies between tickets. To make ticket 34 depend on 22:

	git ticket let 34 need 22

Or

	git ticket let 22 block 34

To undo this:

	git ticket let 34 release 22

To show a tree of the dependencies:

	git ticket list deps
	git ticket list depends
	git ticket list dependencies

### Other Commands

Show info about the current ticket or another ticket:

	git ticket show
	git ticket show 34

Change the current project to another (still fragile):

	git ticket project MYPROJECT

Change the state of a ticket:

	git ticket open 33
	git ticket closed 75
	git ticket invalid 52
	git ticket in-progress 12

Development
-----------

If you would like to change something about git-ticket, make sure you install
using the develop method (see above). Assuming that you already have the repo
cloned, do:

	git checkout develop
	git pull
	git ticket list

This will show all the current tickets. If you find a bug or come up with a
feature, just add it using git-ticket (make sure the ticket branch is synced
before and after doing so). Otherwise, just run

	git ticket start <id>
	git ticket sync

where `<id>` is the ticket id, and start developing! Isn't it fun to be able to
use the thing you're currently coding?
