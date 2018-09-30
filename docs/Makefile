# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = mozzarella
SOURCEDIR     = .
BUILDDIR      = _build
SPHINXDOCBUILD = sphinx-apidoc
SPHINXDOCOPTS  = -f
DOCSSOURCE     = ./api/
PROJECTDIR     = ../acmwebsite


# Put it first so that "make" without argument is like "make help".
help: Makefile
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

clean: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	rm -dr ./api

api:
	$(SPHINXDOCBUILD) -o $(DOCSSOURCE) $(PROJECTDIR) $(SPHINXDOCOPTS)

html: api
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile api
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile api

