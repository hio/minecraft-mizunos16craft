REVISION  ?= m5dev
MCVERSION ?= 1.12
OUTFILE   ?= Mizunos-16-Craft_$(MCVERSION)$(REVISION).zip

gamedir ?= $(HOME)/.minecraft

zip ?= zip

.PHONY: all build

all: build

build:
	rm -f "$(OUTFILE).tmp"
	cd data && $(zip) -r "../$(OUTFILE).tmp" . --exclude '*.xcf' --exclude 'assets/*.txt'
	mv "$(OUTFILE).tmp" "$(OUTFILE)"

install:
	cp "$(OUTFILE)" "$(gamedir)/resourcepacks/$(OUTFILE)"
