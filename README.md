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

List tickets in repo:

	git ticket list

Create a new ticket:

	git ticket new

Start a git flow branch using ticket (the branch type corresponds to the ticket
type) by id:

	git ticket start 34

or by hash:

	git ticket start 64a9g2

Finish the branch (merging as necessary):

	git ticket finish 34

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
