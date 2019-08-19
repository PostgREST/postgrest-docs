#!/usr/bin/env python
from livereload import Server, shell
from subprocess import call
## Build docs at startup
call(['sphinx-build', '-b', 'html', '-a', '-n', '.', '_build'])
server = Server()
server.watch('*.rst', shell('sphinx-build -b html -a -n . _build'))
server.watch('tutorials/*.rst', shell('sphinx-build -b html -a -n . _build'))
server.watch('how-tos/*.rst', shell('sphinx-build -b html -a -n . _build'))
server.serve(root='_build/')
