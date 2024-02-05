# Torrent Scraper
Simple Django webapp that scrapes torrents from popular torrent sites and presents them without the annoyance of ads and popups.
Quearied data is added to a local database so that subsequent searchers are fast and dont require re-scraping the same page multiple times.

The enviroment is in /magnetEnv and managed though venv so,
to start the server run the command:
'''magnetEnv/bin/python3 manage.py runserver'''

Note the webpage is ugly and slow (at least for the first time a given film is queried)
![image](https://github.com/sashamorecode/torrentSraper/assets/34610924/22979f05-0a3b-4d3c-8d73-bf203b886598)

