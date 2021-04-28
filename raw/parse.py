from lingpy import *
from tabulate import tabulate

languages = csv2list('../etc/languages.tsv')

taxa = csv2list('taxa.tsv')

langs = [row[3].strip() for row in languages]

table = []
for row in taxa[1:]:
    if row[2] not in langs and row[2] != '?':
        table += [[row[1], row[2]]]
print(tabulate(table))

