#!/usr/bin/python
import pronouncing
import subprocess
import sys
import json
import random
import re
import sys

def should_display_help():
	if len(sys.argv) == 1 or sys.argv[1] == "--help":
		return True
	else:
		return False

def display_help():
	print("gado - generate poetry using gcc!")
	print()
	print("usage: gado [options] [file] or gado++ [options] [file]")
	print()
	print("tip: you can use gado/gado++ just like gcc/g++!")
	print()
	print("example: gado++ source.cpp -Wall -o output_executable")
	print()
	print("see https://github.com/diksown/gado for more info")

def get_compiler():
	program_name = sys.argv[0]
	if "gado++" in program_name:
		compiler_name = "g++"
	elif "gado" in program_name:
		compiler_name = "gcc"
	else:
		# TODO: treat errors better
		print("error: program name not recognized")
		sys.exit(1)
	return compiler_name

# execute gcc with subprocess and get output
def get_gcc_output():
	json_format = "-fdiagnostics-format=json"
	compiler_name = get_compiler()
	
	# TODO: maybe use some parser instead of this
	gcc_arglist = [compiler_name] + sys.argv[1:] + [json_format]

	gcc_output = subprocess.run(gcc_arglist, capture_output=True)
	error_log = gcc_output.stderr.decode().split('\n')[0]
	
	try:
		error_log_dict = json.loads(error_log)
	except:
		print("error: log is not in json format")
		sys.exit(1)
	
	error_messages = []
	for gcc_error in error_log_dict:
		formatted_error = gcc_error["message"]
		error_messages.append([formatted_error])
	return error_messages
	

# for each line of the output, get the last word
def last_word(line):
	only_alphanum = re.sub("[^0-9a-zA-Z]+", " ", line)
	only_alphanum_lower = only_alphanum.lower()
	only_alphanum_list = only_alphanum_lower.split()
	return only_alphanum_list[-1]

# open the database and get the rhyme for each word
def get_poetry_db():
	with open('/usr/share/gado/data/poetry.json') as poetry_db:
		return json.load(poetry_db)

# get a rhyme using IPA. better rhyme detection, 
# but isn't always possible with words that don't 
# have pronunciations (like fpedantic or int)
def get_phonetic_rhyme(word, poetry_db):
	word_rhymes = pronouncing.rhymes(word)
	verse_rhymes = []
	for word_rhyme in word_rhymes:
		if word_rhyme in poetry_db:
			verse_rhymes.extend(poetry_db[word_rhyme])
	if len(verse_rhymes) != 0:
		return random.choice(verse_rhymes)
	else:
		return None

# define the matching of two words
def match_words(word1, word2):
	max_match = 4
	for i in range(max_match, 0, -1):
		if word1[-i:] == word2[-i:]:
			return i
	return 0

# get a rhyme only comparing the end of the word
# bad quality, but works for words like fpedantic
def get_mirror_rhyme(word, poetry_db):
	# get all keys of poetry_db
	poetry_db_keys = poetry_db.keys()
	# get the number of the biggest match
	max_match = max(map(lambda x: match_words(x, word), poetry_db_keys))
	possible_rhymes = []
	for poetry_db_key in poetry_db_keys:
		if match_words(poetry_db_key, word) == max_match:
			possible_rhymes.extend(poetry_db[poetry_db_key])
	return random.choice(possible_rhymes)


# for each word, get a rhyme at random from the database
def get_rhyme(word, poetry_db):
	rhyme = get_phonetic_rhyme(word, poetry_db)
	if rhyme is not None:
		return rhyme
	else:
		return get_mirror_rhyme(word, poetry_db)

# print formatted rhymes
if __name__ == "__main__":
	if should_display_help():
		display_help()
		sys.exit(0)

	gcc_output = get_gcc_output()
	poetry_db = get_poetry_db()
	for gcc_error in gcc_output:
		error_message = gcc_error[0]
		rhyming_with_error = get_rhyme(last_word(error_message), poetry_db)
		print(rhyming_with_error)
		print(error_message)
		print()
