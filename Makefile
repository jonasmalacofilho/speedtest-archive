install: /usr/bin/speedtest-archive /usr/bin/speedtest-graph crontab

/usr/bin/speedtest-archive:
	sudo cp speedtest-archive.py /usr/bin/speedtest-archive

/usr/bin/speedtest-graph:
	sudo cp speedtest-graph.py /usr/bin/speedtest-graph

uninstall: clear-crontab
	sudo rm -f /usr/bin/speedtest-archive
	sudo rm -f /usr/bin/speedtest-graph

crontab: clear-crontab
	{ crontab -l; echo "*/10 * * * * /usr/bin/speedtest-archive >>~/speedtest_data.tsv 2>>~/.speedtest_archive.log"; } | crontab -
	{ crontab -l; echo "*/30 * * * * /usr/bin/speedtest-graph <~/speedtest_data.tsv >~/speedtest_graph.svg"; } | crontab -

clear-crontab:
	crontab -l | egrep -v "speedtest-(archive|graph)" | crontab -

.PHONY: install uninstall crontab clear-crontab
