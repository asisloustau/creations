import csv
from argparse import ArgumentParser

parse = ArgumentParser()
parse.add_argument('old_file')
parse.add_argument('new_file')
parse.add_argument('--in-delimiter', dest='delim')
parse.add_argument('--in-quote', dest='quote')
argvals = parse.parse_args()

with open(argvals.old_file,newline='') as old_csvfile:
    in_quote = '"'
    in_delim = '|'
    if argvals.delim:
        in_delim = argvals.delim
    if argvals.quote:
        in_quote = argvals.quote
    read_file = csv.reader(old_csvfile, delimiter= in_delim, quotechar= in_quote)
    rows = list(read_file)

with open(argvals.new_file,'w',newline='') as new_csvfile:
    csvwriter = csv.writer(new_csvfile)
    csvwriter.writerows(rows)
