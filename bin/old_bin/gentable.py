#!/usr/bin/env python3
import pandas
from tabulate import tabulate

data = pandas.read_csv('/home/htran/tbl.csv', index_col=0)
#print(tabulate(data, headers=data.columns, tablefmt="grid"))
print(tabulate(data, headers=data.columns, tablefmt="fancy_grid"))

