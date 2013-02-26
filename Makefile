clean:
	find ./ -name \*~ -exec rm {} \; -print
	find ./ -name \*\.pyc -exec rm {} \; -print

reload:
	sudo /etc/init.d/apache2 reload
