#!/usr/bin/python
import pronouncing
import subprocess
import sys
import json
import random
import re
import sys

POETRY_LOCATION = '/usr/share/gado/data/poetry.json'


def should_display_help():
    if len(sys.argv) == 1 or sys.argv[1] == '--help':
        return True
    else:
        return False


def display_help():
    print('gado - generate poetry using gcc!')
    print()
    print('usage: gado [options] [file] or gado++ [options] [file]')
    print()
    print('tip: you can use gado/gado++ just like gcc/g++!')
    print()
    print('example: gado++ source.cpp -Wall -o output_executable')
    print()
    print('see https://github.com/diksown/gado for more info')


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
    something like a dfs.
    return lines and columns if they exist.'''
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
    # execute gcc with subprocess and get output
    json_format = '-fdiagnostics-format=json'
    compiler_name = get_compiler()

    # TODO: maybe use some parser instead of this
    gcc_arglist = [compiler_name] + sys.argv[1:] + [json_format]

    gcc_output = subprocess.run(gcc_arglist, capture_output=True)
    error_log = gcc_output.stderr.decode().split('\n')[0]

    try:
        error_log_dict = json.loads(error_log)
    except:
        print('error: log is not in json format')
        sys.exit(1)

    error_messages = parse_all_gcc_errors(error_log_dict)

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
    '''get a rhyme only comparing the end of the word
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
    '''format the info of a gcc message
    if an error occurs on line 1, column 3, it will
    be formatted as (1, 3) in red'''

    info = ''
    info += '('
    if 'line' in gcc_error:
        info += str(gcc_error['line'])
    if 'column' in gcc_error and gcc_error['column'] != -1:
        info += ':' + str(gcc_error['column'])
    info += ')'

    kind = gcc_error['kind']

    if kind == 'error' or kind == 'fatal_error':
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
        print(info)
        print(rhyme_with_error)
        print(error_message)


def main():
    '''main function'''

    if should_display_help():
        display_help()
        sys.exit(0)

    poetry_db = get_poetry_db()
    gcc_output = get_gcc_output()
    display_poetry(gcc_output, poetry_db)


'''if the script is called directly, call the main function'''
if __name__ == '__main__':
    main()
