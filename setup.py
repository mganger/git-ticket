from setuptools import setup

setup(
	name             = 'git-ticket',
	version          = '0.1',
	description      = 'Ticket managment using git',
	url              = 'http://this.is.a/url',
	author           = 'Michael Ganger',
	author_email     = 'mganger747@gmail.com',
	license          = 'MIT',
	packages         = [ 'gitticket' ],
	package_data     = { 'gitticket': ['commit-msg'] },
	scripts          = [ 'bin/git-ticket' ],
	zip_safe         = False
)
