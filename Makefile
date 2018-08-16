BEEBASM?=beebasm
PYTHON?=python

.PHONY:build
build:
	$(BEEBASM) -i elite-source.asm -v > compile.txt
	$(BEEBASM) -i elite-bcfs.asm -v >> compile.txt
	$(BEEBASM) -i elite-loader.asm -v >> compile.txt
	$(PYTHON) elite-checksum.py -u
	$(BEEBASM) -i elite-disc.asm -do elite.ssd -boot ELITE

.PHONY:verify
verify:
	@$(PYTHON) crc32.py extracted
	@$(PYTHON) crc32.py output

.PHONY:comments
comments: d4090010.txt d4090012.txt
	git checkout -- elite-source.asm
	$(PYTHON) apply-comments.py elite-source.asm $^

%.txt:
	wget http://www.elitehomepage.org/archive/a/$@
	sed -i -e 's/\r$$//' -e 's/\r/\n/' $@
