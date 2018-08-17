from __future__ import print_function
import sys
import re
import os

source_file = sys.argv[1]
commentary_files = sys.argv[2:]
output_file = source_file + '.tmp'

source_label_pattern = re.compile('^\.([A-Z0-9]+)$')
source_instr_pattern = re.compile('^\s+([A-Z]+)(\s+([#&(),0-9A-Z+\\-%]+))?$')
commentary_label_pattern = re.compile(
	'^\t\.([A-Z0-9]+)(\s+\\\\\s+->\s+&([0-9A-F]+))?(\s+\\\\\s+(.*))?$')
commentary_instr_pattern = re.compile(
	'^(([0-9A-F]{2})\s){1,3}\s+([A-Z]+)(\s+([#&,0-9A-Z]+))?\s*(\\\\\s+(.*))?$')

label_comments = {}
label_instructions = {}

for commentary_file in commentary_files:
	name = None
	for line in open(commentary_file):
		line = line.rstrip()
		match = commentary_label_pattern.match(line)
		if match:
			name = match.group(1)
			comment = match.group(5)
			if comment:
				label_comments[name] = comment
			label_instructions[name] = []
			continue
		match = commentary_instr_pattern.match(line)
		if match:
			instr = match.group(3)
			argument = match.group(5)
			comment = match.group(7)
			if name:
				label_instructions[name].append((instr, argument, comment))

output = open(source_file + '.tmp', 'w')

name = None
for line in open(source_file):
	line = line.rstrip()
	match = source_label_pattern.match(line)
	if match:
		name = match.group(1)
		if name in label_comments:
			print(".%s ; %s" % (name, label_comments[name]), file=output)
			continue
	match = source_instr_pattern.match(line)
	if match:
		instr = match.group(1)
		argument = match.group(3)
		if name in label_instructions:
			seq = label_instructions[name]
			if len(seq) != 0:
				c_instr, c_argument, c_comment = seq.pop(0)
				if instr == c_instr and c_comment:
					if argument:
						result = " %s %s ; %s" % (instr, argument, c_comment)
					else:
						result = " %s ; %s" % (instr, c_comment)
					print(result, file=output)
					continue
	print(line, file=output)

output.close()
os.rename(output_file, source_file)
