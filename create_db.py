#!/usr/bin/python
import json
import re

def valid_line(line):
	if len(line) < 30 or len(line) > 65: # too short or too long lines
		return False
	if line.upper() == line: # all caps
		return False
	return True

def last_word(line):
	only_alphanum = re.sub("[^0-9a-zA-Z]+", " ", line)
	only_alphanum_lower = only_alphanum.lower()
	only_alphanum_list = only_alphanum_lower.split()
	return only_alphanum_list[-1]

dict_poetry_db = {}

# TODO: improve these hardcoded paths
with open('/usr/share/gado/data/shakespeare.txt') as poetry_data:
	for line in poetry_data.readlines():
		line = line.strip()
		if valid_line(line):
			representative_word = last_word(line)
			dict_poetry_db.setdefault(representative_word, []).append(line)

json.dump(dict_poetry_db, open('/usr/share/gado/data/poetry.json', 'w'), indent=2)