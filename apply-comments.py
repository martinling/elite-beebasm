from __future__ import print_function
import sys
import re
import os

source_file = sys.argv[1]
commentary_files = sys.argv[2:]
output_file = source_file + '.tmp'

source_label_pattern = re.compile('^\.([A-Z0-9]+)$')
commentary_label_pattern = re.compile(
	'^\t\.([A-Z0-9]+)(\s+\\\\\s+->\s+&([0-9A-F]+))?(\s+\\\\\s+(.*))?$')

label_comments = {}

for commentary_file in commentary_files:
	for line in open(commentary_file):
		line = line.rstrip()
		match = commentary_label_pattern.match(line)
		if match:
			name = match.group(1)
			comment = match.group(5)
			if comment:
				label_comments[name] = comment

output = open(source_file + '.tmp', 'w')

for line in open(source_file):
	line = line.rstrip()
	match = source_label_pattern.match(line)
	if match:
		name = match.group(1)
		if name in label_comments:
			print(".%s ; %s" % (name, label_comments[name]), file=output)
			continue
	print(line, file=output)

output.close()
os.rename(output_file, source_file)
