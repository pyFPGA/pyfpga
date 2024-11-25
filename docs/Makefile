SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = build
HELPERS       = $(BUILDDIR)/hdl2bit $(BUILDDIR)/prj2bit $(BUILDDIR)/bitprog

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

$(HELPERS):
	@mkdir -p $(@D)
	@python3 ../pyfpga/helpers/$(@F).py -h > $@

%: Makefile $(HELPERS)
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
