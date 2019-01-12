FILE=poster

all:
	xelatex -shell-escape $(FILE).tex
	biber $(FILE)
	xelatex -shell-escape $(FILE).tex

clean:
	rm -rf $(FILE).aux $(FILE).bcf $(FILE).log $(FILE).out $(FILE).run.xml
	rm -rf $(FILE).bbl $(FILE).blg texput.log _minted-$(FILE)
	rm -rf $(FILE).toc $(FILE).nav $(FILE).snm
