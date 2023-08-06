#!/usr/bin/python3

with open('mature.fa') as infile:
	for line in infile:
		if line.startswith(">"):
			name = line.strip().split()[0].replace('>', '')
			print(name)	
