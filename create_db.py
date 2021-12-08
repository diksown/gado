#!/usr/bin/python
import json
import re


# TODO: improve these hardcoded paths
POETRY_SOURCE = '/usr/share/gado/data/shakespeare.txt'
POETRY_LOCATION = '/usr/share/gado/data/poetry.json'


def valid_line(line):
    # too short or too long lines are not valid
    if len(line) < 30 or len(line) > 60:
        return False
    # all caps lines are not valid
    if line.upper() == line:
        return False
    return True


def last_word(line):
    only_alphanum = re.sub("[^a-zA-Z]+", " ", line)
    only_alphanum_lower = only_alphanum.lower()
    only_alphanum_list = only_alphanum_lower.split()
    return only_alphanum_list[-1]


dict_poetry_db = {}

with open(POETRY_SOURCE) as poetry_data:
    for line in poetry_data.readlines():
        line = line.strip()
        if valid_line(line):
            representative_word = last_word(line)
            dict_poetry_db.setdefault(representative_word, []).append(line)

json.dump(dict_poetry_db, open(POETRY_LOCATION, 'w'), indent=2)
