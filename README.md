Git-Ticket
==========

Git-ticket is intended to be a full-featured distributed ticketing system. It is
inspired in large part by ticgit-ng.

Dependencies
------------
git-flow
GitPython

Installation
------------

To install, just go to the root directory and run:

	make install

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
