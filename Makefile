REVISION = m2
MCVERSION = 1.12
OUTFILE = Mizunos-16-Craft_$(MCVERSION)$(REVISION).zip

zip ?= zip

.PHONY: all build

all: build

build:
	rm -f "$(OUTFILE).tmp"
	cd data && $(ZIP) -r "../$(OUTFILE).tmp" .
	mv "$(OUTFILE).tmp" "$(OUTFILE)"
