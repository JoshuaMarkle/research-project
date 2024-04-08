# Makefile

run:
	cd src && python main.py

pdf:
	rm research.pdf
	pandoc research.md --output=research.pdf --pdf-engine=xelatex
