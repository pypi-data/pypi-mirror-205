'''
Created on 2010-11-26
New module created on 2013-03-16

@author: Torsten Hahmann
'''

from pyparsing import nestedExpr, ParseException
import macleod_eureka.Filemgt as filemgt
import os
import logging
import math

CLIF_IMPORT = 'cl-imports'

CLIF_COMMENT = 'cl-comment'

CLIF_MODULE = 'cl-module'

CLIF_TEXT = 'cl-text'

# CLIF symbols that are logically irrelevant
CLIF_OTHER_SYMBOLS = set([CLIF_IMPORT, CLIF_COMMENT, CLIF_MODULE, CLIF_TEXT])

CLIF_EXISTENTIAL = 'exists'

CLIF_UNIVERSAL = 'forall'

# logical connectives in CLIF
CLIF_LOGICAL_CONNECTIVES = set(
    ['not', 'and', 'or', 'iff', 'if', '=', CLIF_EXISTENTIAL, CLIF_UNIVERSAL])

CLIF_QUANTIFIERS = set([CLIF_EXISTENTIAL, CLIF_UNIVERSAL])

# TPTP equivalents for CLIF connectives

TPTP_UNARY_SUBSTITUTIONS = {'not': '~'}

TPTP_NARY_SUBSTITUTIONS = {'and': '&', 'or': '|'}

TPTP_BINARY_SUBSTITUTIONS = {'iff': '<=>', 'if': '=>'}

TPTP_QUANTIFIER_SUBSTITUTIONS = {CLIF_UNIVERSAL: '!', CLIF_EXISTENTIAL: '?'}

TPTP_SUBSTITUTIONS = [TPTP_UNARY_SUBSTITUTIONS, TPTP_NARY_SUBSTITUTIONS,
                      TPTP_BINARY_SUBSTITUTIONS, TPTP_QUANTIFIER_SUBSTITUTIONS]

# LADR (PROVER9) equivalents for CLIF connectives

LADR_UNARY_SUBSTITUTIONS = {'not': '-'}

LADR_NARY_SUBSTITUTIONS = {'and': '&', 'or': '|'}

LADR_BINARY_SUBSTITUTIONS = {'iff': '<->', 'if': '->'}

LADR_QUANTIFIER_SUBSTITUTIONS = {
    CLIF_UNIVERSAL: 'all', CLIF_EXISTENTIAL: 'exists'}

LADR_SUBSTITUTIONS = [LADR_UNARY_SUBSTITUTIONS, LADR_NARY_SUBSTITUTIONS,
                      LADR_BINARY_SUBSTITUTIONS, LADR_QUANTIFIER_SUBSTITUTIONS]

# TODO: need to read translations from file
SYMBOL_TRANSLATIONS = {'<': 'lt',
                       '>': 'gt',
                       '<=': 'leq',
                       '>=': 'geq'}

SYMBOL_AUTO_NAME = 'clifsym'

SYMBOL_AUTO_NUM = 1


def remove_all_comments(input_file, output_file):
    """Remove all comments (multi-line and single-line comments), including cl-comment blocks from the given CLIF single_file.
    Parameters:
    input_file -- filename of the CLIF input
    output_file -- filename where to write the CLIF single_file removed of comments."""

    def strip_sections(lines, begin_symbol, end_symbol):
        """Remove sections that start with the begin_symbol and end with end_symbol"""
        output = []
        if len(lines) == 0:
            return output
        line = lines.pop(0)
        # variable to denote that we are currently within a multiline section
        within_section = False
        outline = ""
        start = ""
        while True:
            if within_section and end_symbol not in line:
                # ignore line: do not write to output
                if len(output) > 0:
                    output.append(outline)
                outline = ""
                if len(lines) > 0:
                    line = lines.pop(0)
                else:
                    output.append(start)
                    raise ClifParsingError('Syntax error in clif input: no matching' + end_symbol +
                                           ' for ' + begin_symbol + ' on line ' + str(len(output) + 1), output)
            elif within_section and end_symbol in line:
                within_section = False
                # normally process the remainder
                line = line.split(end_symbol, 1)
                if len(line) > 0:
                    line = line[1]
            elif not within_section and begin_symbol in line:
                within_section = True
                line = line.split(begin_symbol, 1)
                start = line[0]
                outline = line[0] + '\n'
                if len(line[1]) > 1:
                    line = line[1]
            else:
                # copy line to output
                outline += line
                output.append(outline)
                outline = ""
                if len(lines) > 0:
                    line = lines.pop(0)
                else:
                    return output

    def strip_clif_comments(lines):
        output = []
        if len(lines) == 0:
            return output
        line = lines.pop(0)
        outline = ""
        search_end = False
        start = ""
        while True:
            if search_end:
                # searching for the closing quotes
                line = line.split('\'', 1)
                if len(line) > 1:
                    # closing quotes found in line
                    search_end = False
                    line = line[1].split(')', 1)
                    if len(line) < 2:
                        output.append(start)
                        raise ClifParsingError('Syntax error in clif input: no closing parenthesis found for ' +
                                               CLIF_COMMENT + ' on line ' + str(len(output) + 1), output)
                    if len(line[0].strip()) > 0:
                        output.append(start)
                        raise ClifParsingError('Syntax error in clif input: found illegal characters before closing parenthesis in ' +
                                               CLIF_COMMENT + ' on line ' + str(len(output) + 1), output)
                    outline += line[1]
                    output.append(outline)
                    outline = ""
                    if len(lines) > 0:
                        line = lines.pop(0)
                    else:
                        return output
                else:
                    # no closing quotes found in line, proceed to next line
                    outline = ""
                    if len(lines) > 0:
                        line = lines.pop(0)
                    else:
                        output.append(start)
                        raise ClifParsingError('Syntax error in clif input: missing closing quotes for ' +
                                               CLIF_COMMENT + ' on line ' + str(len(output) + 1), output)
            elif CLIF_COMMENT not in line:
                # just copy the line to output
                outline += line
                output.append(outline)
                outline = ""
                if len(lines) > 0:
                    line = lines.pop(0)
                else:
                    return output
            else:
                # found a cl-comment
                parts = line.split(CLIF_COMMENT, 1)
                parts2 = parts[0].rsplit('(', 1)
                start = line
                if len(parts2) < 2:
                    output.append(start)
                    raise ClifParsingError('Syntax error in clif input: no opening parenthesis found before ' +
                                           CLIF_COMMENT + ' on line ' + str(len(output) + 1), output)
                if len(parts[0].strip()) > 1:
                    output.append(parts[0][0:-1] + '\n')
                # searching for the begin of the comment quotes
                line = parts[1].split('\'', 1)
                if len(line[0].strip()) > 0:
                    output.append(start)
                    raise ClifParsingError('Syntax error in clif input: found illegal characters after ' +
                                           CLIF_COMMENT + ' on line ' + str(len(output) + 1), output)
                line = line[1]
                search_end = True

    def strip_lines(lines, begin_symbol):
        """Remove comments that start with begin_symbol."""
        output = []
        for line in lines:
            newline = line.split(begin_symbol, 1)[0]
            if len(newline) < len(line):
                output.append(newline + '\n')
            else:
                output.append(newline)
        return output

    # MAIN METHOD remove_all_comments()
    lines = []

    with open(input_file, 'r') as single_file:
        try:
            lines = single_file.readlines()
            # DO stuff
            lines = strip_sections(lines, '/*', '*/')
            lines = strip_clif_comments(lines)
            lines = strip_lines(lines, ';')
        except IOError:
            single_file.close()
        except ClifParsingError as e:
            logging.getLogger(__name__).error(e)
            single_file.close()
            lines = []
        finally:
            single_file.close()

    with open(output_file, 'w+') as single_file:
        logging.getLogger(__name__).debug(
            "Writing to " + os.path.abspath(output_file))
        try:
            single_file.writelines(lines)
        except IOError:
            single_file.close()
        finally:
            single_file.close()


def reformat_urls(lines):
    """Delete URL prefixes from all import declarations."""
    lines = list(lines)
    prefixes = filemgt.read_config('cl', 'prefix').split(',')
    prefixes = [p.strip().strip('"') for p in prefixes]
    prefixes = sorted([p.strip() for p in prefixes],
                      key=lambda s: len(s), reverse=True)
    for i in range(0, len(lines)):
        for prefix in prefixes:
            if prefix in lines[i]:
                if not prefix.endswith('/'):
                    prefix = prefix + '/'
                # print "replacing prefix: " + prefix + " in " + lines[i]
                lines[i] = lines[i].replace(prefix, '')
                # print lines[i]
    return lines


def get_all_nonlogical_symbols(filename):
    nonlogical_symbols = set([])
    sentences = get_logical_sentences_from_file(filename)
    for sentence in sentences:
        # print "SENTENCE = " + sentence
        nonlogical_symbols.update(get_nonlogical_symbols(sentence))
    logging.getLogger(__name__).debug(
        "Nonlogical symbols: " + str(nonlogical_symbols))
    return nonlogical_symbols


def get_sentences_from_file(input_file_name):
    """ extract all Clif sentences from a Clif input single_file and returns the sentences as a list of strings. This set of sentences includes, e.g., import declarations."""
    #print("NAME = " + input_file_name)
    cl_file = open(input_file_name, 'r')
    text = cl_file.readlines()
    text = reformat_urls(text)
    cl_file.close()
    text = "".join(text)    # compile into a single string
    sentences = get_sentences(text)
    return sentences


def get_logical_sentences_from_file(input_file_name):
    """ extract all Clif sentences from a Clif input single_file and returns the sentences as a list of strings. This set excludes sentences that are not logical sentences, such as import declarations."""
    sentences = get_sentences_from_file(input_file_name)

    logical_sentences = []

    for s in sentences:
        if len(s) == 2 and s[0] in CLIF_OTHER_SYMBOLS:
            continue
        else:
            logical_sentences.append(s)

    # print input_file_name + " HAS SENTENCES " + str(logical_sentences)

    return logical_sentences


def get_sentences(text):

    def flatten_sentence(pieces):
        # base case: no list and just a single element
        if isinstance(pieces, str):
            return pieces
        elif len(pieces) == 1:
            if isinstance(pieces[0], str):
                return [pieces[0]]
            else:
                return flatten_sentence(pieces[0])
        # induction
        # print "flattening " + str(pieces)
        return [flatten_sentence(piece) for piece in pieces]

    try:
        pieces = nestedExpr('(', ')').parseString(text)
    except ParseException as e:
        logging.getLogger(__name__).error(e)
        raise ClifParsingError(
            "input is not valid Clif format, ensure that parentheses match\n\n" + text)
        return
    if len(pieces) != 1:
        raise ClifParsingError(
            "input is not valid Clif format, ensure that parentheses match\n\n" + text)
        return
    pieces = flatten_sentence(pieces)
    while True:
        # print str(piece) + " is " + str(type(piece))
        if isinstance(pieces[0], str):
            # print "REMOVING "+ pieces[0]
            # remove "cl-module/ cl-text statement at the beginning"
            pieces.pop(0)
        else:
            break

#    for piece in pieces:
#        print 'SENTENCE: ' + str(piece) + '\n'

    return pieces


def get_nonlogical_symbols_and_variables(sentence):
    """Extract all nonlogical symbols and variables from a logical sentence in CLIF notation."""

    def get_all_symbols(pieces):
        symbols = set([])
        for p in pieces:
            if isinstance(p, str):
                symbols.add(p)
            else:
                symbols.update(get_all_symbols(p))
        return symbols

    symbols = get_all_symbols(sentence)
    # print "SYMBOLS = " + str(symbols)
    variables = get_variables(sentence)

    # print "ALL VARIABLES = " + str(variables)

    return (symbols - set(CLIF_LOGICAL_CONNECTIVES) - set(CLIF_OTHER_SYMBOLS) - set(['']) - variables, variables)


def get_nonlogical_symbols(sentence):
    """Extract all nonlogical symbols from a logical sentence in CLIF notation."""
    (non_logical_symbols, _) = get_nonlogical_symbols_and_variables(sentence)
    return non_logical_symbols


def get_variables(sentence):
    """Extract the variables from a logical sentence in CLIF notation."""
    variables = set([])

    # print "EXTRACTING VARIABLES FROM " + str(sentence)
    pieces = sentence[:]

    if len(pieces) == 0 or isinstance(pieces, str):
        return variables

    if isinstance(pieces[0], str):
        # print sentence[0]
        for q in CLIF_QUANTIFIERS:
            if pieces[0] == q:
                # print "FOUND " + q + ": " + str(pieces[1])
                variables.update(pieces[1])
                pieces.pop(0)
                pieces.pop(0)
                variables.update(get_variables(pieces))
                return variables
        pieces.pop(0)
        if len(pieces) > 0:
            variables.update(get_variables(pieces))
        return variables

    for i in range(0, len(pieces)):
        variables.update(get_variables(pieces[i]))
    # print "VARIABLES = " + str(variables)
    return variables

def get_nonlogical_symbol_arity_from_file(input_file_name, symbol):
    """
    Evaluate and return the arity of a symbol as defined in a specific file.
    Interface to maintain backwards compatibility with rest of Macleod code
    base.

    :param str input_file_name
    :param str symbol
    :return The arity of a passed symbol
    :rtype int
    """


    sentences = get_logical_sentences_from_file(input_file_name)
    arity = get_nonlogical_symbol_arity(sentences, symbol, None)
    if arity is None:
        arity = 0
    logging.getLogger(__name__).debug("Nonlogical symbol: " + symbol + " has arity " + str(arity))

    return arity

def get_nonlogical_symbol_arity(pieces, symbol, arity):
    """
    Recursively find sentence fragments that start with the sought-after
    symbol and return its arity if found.

    IMPORTANT TO NOTE THIS MODIFIES STUFF IN PLACE

    :param list() pieces
    :return Arity of passed symbol
    :rtype int()
    """

    if isinstance(pieces, str):
        return arity
    elif isinstance(pieces[0], str):
        found_symbol = pieces[0]
        del pieces[0]
        if found_symbol == symbol:
            if arity is None:
                #logging.getLogger(__name__).debug("Nonlogical symbol: " + symbol + " number of pieces =" + str(len(pieces)) )
                arity = len(pieces)  # set the arity
                #logging.getLogger(__name__).info("Nonlogical symbol: " + symbol + " has arity " + str(arity))
            elif arity != len(pieces):
                raise ClifParsingError(
                    "the symbol " + symbol + " is used with two different arities: " + str(arity) + " and " + str(len(pieces)))
                return False
    # recursion
    for i in range(len(pieces)):
        arity = get_nonlogical_symbol_arity(pieces[i], symbol, arity)

    return arity



def get_imports(input_file):
    """Find all the imported modules from a CLIF single_file.
    Parameters:
    input_file -- filename of the CLIF input."""

    imports = set([])

    sentences = get_sentences_from_file(input_file)
    for s in sentences:
        if len(s) == 2 and s[0] == CLIF_IMPORT:
            imports.add(filemgt.get_canonical_relative_path(s[1]))

    # print "IMPORTS = " + str(imports)
    return imports


class ClifParsingError(Exception):

    output = []

    def __init__(self, value, output=[]):
        self.value = value
        self.output = output
        while None in self.output:
            self.output.remove(None)
        while '' in self.output:
            self.output.remove('')
        while '\r\n' in self.output:
            self.output.remove('\r\n')
        # print "ERROR OUTPUT = " + str(self.output)

    def __str__(self):
        if len(self.output) == 0:
            return repr(self.value) + '\n'
        else:
            return repr(self.value) + '\n' + (''.join(self.output))


if __name__ == '__main__':
    import sys
    # global variables
    options = sys.argv
    remove_all_comments(options[1], options[2])
