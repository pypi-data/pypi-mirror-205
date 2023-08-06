#!/usr/bin/env python3

maturefa_names = set()
mirna_names = set()
with open('mirbase_names_maturefa.txt') as infile:
	for name in infile:
		maturefa_names.add(name.strip())

with open('mirbase_names_xls.txt') as infile:
	for name in infile:
		mirna_names.add(name.strip())

common = maturefa_names.intersection(mirna_names)
mf_notin_xls = maturefa_names.difference(mirna_names)
xls_notin_mf = mirna_names.difference(maturefa_names)
print("# common: %d" % len(common))
print("# mature fa not in xls: %d" % len(mf_notin_xls))
print("# xls not in mature fa: %d" % len(xls_notin_mf))
with open('common.txt', 'w') as outfile:
	for name in sorted(common):
		outfile.write('%s\n' % name)
