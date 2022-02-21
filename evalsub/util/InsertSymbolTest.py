# coding: utf-8
DESCRIPTION = """
The script breaks sentences before a maximum length is reached. Selection of type of break <eol> or <eob> 
is done randomly.
"""

try:
    from itertools import izip as zip
except ImportError:  # will be 3.x series
    pass
from os.path import join
import argparse
import random


MAX_POS = 42


def insert_symbol(in_str: str, max_pos: int, symbol: str = '<eob>') -> str:

    # If the string is too short, just return it
    if len(in_str) <= max_pos:
        return str(in_str + ' ' + symbol)

    buffer = []
    while len(in_str) > max_pos:
        # Look for the first space from the max length backwards to the beginning
        in_str_before = in_str[0:max_pos]
        #print(in_str_before)
        first_space_pos = in_str_before[::-1].find(' ')
        #print(first_space_pos)

        # No space?Just return the input string
        # if first_space_pos == -1:
            # return str(in_str + symbol)

        # Compute the space position in the non-reversed string
        last_space_pos = max_pos - first_space_pos
        #print(last_space_pos)

        # Select type of symbol randomly
        roll = random.random()
        if roll < 0.5:
            symbol = '<eol>'
        else:
            symbol = '<eob>'
        # Insert the symbol and return
        buffer.append(in_str[0:last_space_pos] + symbol)  # + in_str[last_space_pos:]
        in_str = in_str[last_space_pos:]
        #print(in_str)
    # Last break must be an <eob>
    buffer.append(in_str + ' <eob>')
    out = ' '.join(buffer)
    return out


def parse_args():
    parser = argparse.ArgumentParser(description=DESCRIPTION)

    parser.add_argument('--input_file', '-if', type=str,
                        help="Text file with sentences")
    parser.add_argument('--output_file', '-of', type=str,
                        help="Text file with sentences separated by symbols")

    args = parser.parse_args()
    return args


def main(args):
    infile = args.input_file
    outfile = args.output_file
    
    with open(infile, 'r') as inf, open(outfile, 'w') as w:
        for line in inf:
            line = line.strip()
            s2 = insert_symbol(in_str=line, max_pos=MAX_POS)
            print("Input string: '{}'".format(line))
            #print("Truncated   : '{}'".format(line[0:MAX_POS]))
            print("With symbols : '{}'".format(s2))
            w.write(s2 + '\n')


if __name__ == '__main__':
    main(parse_args())