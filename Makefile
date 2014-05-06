install: /usr/bin/speedtest-archive crontab

/usr/bin/speedtest-archive:
	sudo cp speedtest-archive.py /usr/bin/speedtest-archive

uninstall: clear-crontab
	sudo rm /usr/bin/speedtest-archive

crontab: clear-crontab
	{ crontab -l; echo "*/10 * * * * /usr/bin/speedtest-archive >> ~/.speedtest_archive.tsv 2>~/.speedtest_archive.err"; } | crontab -

clear-crontab:
	crontab -l | grep -v speedtest-archive | crontab -

.PHONY: install uninstall crontab clear-crontab
