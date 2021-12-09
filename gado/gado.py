#!/usr/bin/python
import json
import os
import random
import re
import subprocess
import sys

import pronouncing
import requests
from xdg.BaseDirectory import xdg_cache_home as cache_home

# TODO: improve these hardcoded values!
DATABASE_URL = 'https://www.gutenberg.org/files/100/100-0.txt'
GADO_CACHE = cache_home + '/gado'
POETRY_LOCATION = GADO_CACHE + '/poetry.json'


def should_display_help():
    if len(sys.argv) == 1 or sys.argv[1] == '--help':
        return True
    else:
        return False


def display_help():
    '''display help message'''
    message = '''gado - generate poetry using gcc!

    usage: gado [options] [file] or gado++ [options] [file]

    tip: you can use gado/gado++ just like gcc/g++!

    example: gado++ source.cpp -Wall -o output_executable

    see https://github.com/diksown/gado for more info
    '''
    print(message)


def get_compiler():
    program_name = sys.argv[0]
    if 'gado++' in program_name:
        compiler_name = 'g++'
    elif 'gado' in program_name:
        compiler_name = 'gcc'
    else:
        # TODO: treat errors better
        print('error: program name not recognized')
        sys.exit(1)
    return compiler_name


def parse_gcc_error(error_log_dict):
    '''recursively parse error messages, getting line and column numbers.

    something like a dfs. return lines and columns if they exist.'''
    messages = []

    # TODO: When adding support to file names, adding 'note'
    # to relevant_kinds will be useful. for now, notes are
    # kind of confusing.
    relevant_kinds = ['error', 'warning', 'fatal error']

    if error_log_dict['kind'] in relevant_kinds:
        gcc_error = {}
        gcc_error['message'] = error_log_dict['message']
        gcc_error['kind'] = error_log_dict['kind']
        locations = error_log_dict['locations']
        if len(locations) != 0:
            gcc_error['line'] = locations[0]['caret']['line']
            gcc_error['column'] = locations[0]['caret']['column']
        messages.append(gcc_error)

    if 'children' in error_log_dict:
        for child in error_log_dict['children']:
            child_messages = parse_gcc_error(child)
            messages.extend(child_messages)
    return messages


def parse_all_gcc_errors(error_logs):
    '''calls the recursive function for each element of the array'''
    messages = []
    for error_log in error_logs:
        messages.extend(parse_gcc_error(error_log))
    return messages


def get_gcc_output():
    '''execute gcc with subprocess and get output'''
    json_format = '-fdiagnostics-format=json'
    compiler_name = get_compiler()

    gcc_arglist = [compiler_name] + sys.argv[1:] + [json_format]

    gcc_output = subprocess.run(gcc_arglist, capture_output=True)
    error_log = gcc_output.stderr.decode().split('\n')[0]

    try:
        error_log_dict = json.loads(error_log)
        error_messages = parse_all_gcc_errors(error_log_dict)
    except:
        # TODO: this is kinda hardcoded
        error_messages = [{"message": error_log, "kind": "error"}]

    return error_messages


def last_word(line):
    '''for each line of the output, get the last word'''
    only_alphanum = re.sub('[^a-zA-Z]+', ' ', line)
    only_alphanum_lower = only_alphanum.lower()
    only_alphanum_list = only_alphanum_lower.split()
    return only_alphanum_list[-1]


def get_poetry_db():
    '''open the database and get the rhyme for each word'''
    with open(POETRY_LOCATION) as poetry_db:
        return json.load(poetry_db)


def get_phonetic_rhyme(word, poetry_db):
    '''get a rhyme using IPA. better rhyme detection,
    but isn't always possible with words that don't
    have pronunciations (like fpedantic or int)'''
    word_rhymes = pronouncing.rhymes(word)
    verse_rhymes = []
    for word_rhyme in word_rhymes:
        if word_rhyme in poetry_db:
            verse_rhymes.extend(poetry_db[word_rhyme])
    if len(verse_rhymes) != 0:
        return random.choice(verse_rhymes)
    else:
        return None


def match_words(word1, word2):
    '''define the matching of two words'''
    max_match = 4
    max_match_to_try = min(max_match, len(word1), len(word2))
    for i in range(max_match_to_try, 0, -1):
        if word1[-i:] == word2[-i:]:
            return i
    return 0


def get_mirror_rhyme(word, poetry_db):
    '''get a rhyme only comparing the end of the word.
    bad quality, but works for words like fpedantic'''
    poetry_db_keys = poetry_db.keys()
    # get the number of the biggest match
    max_match = max(map(lambda x: match_words(x, word), poetry_db_keys))
    possible_rhymes = []
    for poetry_db_key in poetry_db_keys:
        if match_words(poetry_db_key, word) == max_match:
            possible_rhymes.extend(poetry_db[poetry_db_key])
    return random.choice(possible_rhymes)


def get_rhyme(word, poetry_db):
    '''for each word, get a rhyme at random from the database'''
    rhyme = get_phonetic_rhyme(word, poetry_db)
    if rhyme is not None:
        return rhyme
    else:
        return get_mirror_rhyme(word, poetry_db)


def color_it(message, color):
    '''colorize a message'''
    colors = {
        'RED': '\u001b[31m',
        'LIGHT_RED': '\u001b[31;1m',
        'MAGENTA': '\u001b[35m',
        'YELLOW': '\u001b[33m',
        'RESET': '\u001b[0m'
    }
    return colors[color] + message + colors['RESET']


def formatted_info(gcc_error):
    '''format the info of a gcc message.
    if an error occurs on line 1, column 3, it will
    be formatted as (1, 3) in red'''

    kind = gcc_error['kind']

    info = ''
    info += '('
    should_add_space = False
    if 'line' in gcc_error:
        info += str(gcc_error['line']) + ':'
        should_add_space = True
    if 'column' in gcc_error and gcc_error['column'] != -1:
        info += str(gcc_error['column']) + ':'
        should_add_space = True
    if should_add_space:
        info += ' '
    info += kind
    info += ')'

    if kind == 'error' or kind == 'fatal error':
        return color_it(info, 'RED')
    elif kind == 'warning':
        return color_it(info, 'MAGENTA')
    elif kind == 'note':
        return color_it(info, 'YELLOW')
    else:
        return info


def display_poetry(gcc_output, poetry_db):
    '''find rhymes and display them'''
    flag_enter = False
    for gcc_error in gcc_output:
        if flag_enter:
            print()
        else:
            flag_enter = True
        error_message = gcc_error['message']
        rhyme_with_error = get_rhyme(last_word(error_message), poetry_db)
        info = formatted_info(gcc_error)

        print(rhyme_with_error)
        print(error_message)
        print(info)


def valid_line(line):
    '''check if the line is valid for our purposes'''
    # too short or too long lines are not valid
    if len(line) < 30 or len(line) > 60:
        return False
    # all caps lines are not valid
    if line.upper() == line:
        return False
    return True


def process_poetry_database(poetry_data):
    '''receive a raw .txt and process it to a dictionary'''
    dict_poetry_db = {}

    poetry_data_lines = poetry_data.split('\n')

    for line in poetry_data_lines:
        line = line.strip()
        if valid_line(line):
            repr_word = last_word(line)
            dict_poetry_db.setdefault(repr_word, []).append(line)

    return dict_poetry_db


def download_poetry():
    '''download and save the poetry database'''

    # TODO: display a progress bar
    # TODO: try except for the download

    print("downloading poetry. this will only happen once (~5.5MB)")
    poetry_data_req = requests.get(DATABASE_URL)
    poetry_data = poetry_data_req.content.decode()
    dict_poetry_db = process_poetry_database(poetry_data)
    json.dump(dict_poetry_db, open(POETRY_LOCATION, 'w'), indent=2)


def check_for_database():
    '''check if the poetry database exists'''
    # TODO: improve this!
    if not os.path.isfile(POETRY_LOCATION):
        os.makedirs(GADO_CACHE, exist_ok=True)
        download_poetry()


def main():
    '''main function'''

    check_for_database()

    if should_display_help():
        display_help()
        sys.exit(0)

    poetry_db = get_poetry_db()
    gcc_output = get_gcc_output()
    display_poetry(gcc_output, poetry_db)


if __name__ == '__main__':
    main()
