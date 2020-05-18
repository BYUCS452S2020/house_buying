# Docker file to easily set up the MySQL server

**For linux users**\
Go to the directory that the docker-compose file is in. Type in this command:

	sudo docker-compose up -d
  
To turn off the server do this:

	sudo docker-compose down
  
**For Mac users**\
Sorry I have no idea. Probably pretty similar to Linux

**For Windows users**\
Good luck idk.


# Python environment

(use python3)

	mkdir ~/venvs/cs452
	python3 -m venv ~/venvs/cs452
	source ~/venvs/cs452/bin/activate
	pip3 install mysql-connection-python
you should be good to go
	
