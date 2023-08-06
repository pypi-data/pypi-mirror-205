#!/usr/bin/env python3

import pandas

df = pandas.read_csv('miRNA.csv', sep='\t', header=0)
mirna_names = list(df['ID'])
for name in mirna_names:
	print(name)
