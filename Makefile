REVISION  ?= m8
MCVERSION ?= 1.12
OUTFILE   ?= Mizunos-16-Craft-$(MCVERSION)-$(REVISION).zip

gamedir ?= $(HOME)/.minecraft
all_mcversions = \
	1.12   \
	1.11.2 \
	1.10.2 \
	1.9.4  \
	1.8.9  \
	$(NULL)

ZIP ?= zip
SED ?= sed
PYTHON ?= python3

.PHONY: all build build-all purge install inplace-build

all: build

substitute = \
	case "$(MCVERSION)" in \
		1.[78]*)   pack_format=1 ;; \
		1.9*)      pack_format=2 ;; \
		1.10*)     pack_format=2 ;; \
		1.1[1-9]*) pack_format=3 ;; \
		*) : "pack_format not known for mcversion [$(MCVERSION)]"; exit 1;; \
	esac && \
	$(SED) \
		-e 's/@pack_format@/'$$pack_format'/g' \
		-e 's/@revision@/$(REVISION)/g' \
		-e 's/@mcversion@/$(MCVERSION)/g'

_build:
	mkdir $@

.PHONY: FORCE
FORCE:
_build/Mizunos-16-Craft-%.zip: FORCE | _build
	@set -e -u -x; \
outname="$(@F:%.zip=%)"; \
rm -f $@.tmp; \
rsync -rv --include 'readme.txt' --exclude '*.in' --exclude '*.xcf' --exclude '*.txt' --exclude '*.py' --exclude '*.in' ./data/ "./_build/$$outname/"; \
rm -f ./_build/$$outname/assets/minecraft/textures/entity/bed/bed-frame.png; \
rm -f ./_build/$$outname/assets/minecraft/textures/entity/bed/bed-mask.png; \
$(substitute) < data/pack.mcmeta.in > ./_build/$$outname/pack.mcmeta; \
(cd "./_build/$$outname" && $(ZIP) -r "../$$outname.zip.tmp" .); \
mv "_build/$$outname.zip.tmp" "_build/$$outname.zip"; \
rm -rf "./_build/$$outname"; \
: "done"

purge:
	rm -rf _build

build: _build/$(OUTFILE)

build-all: $(all_mcversions:%=do-build-%)

do-build-%: | _build
	$(MAKE) MCVERSION=$(@:do-build-%=%) > _build/Mizunos-16-Craft-$(@:do-build-%=%)-$(REVISION).log 2>&1

install:
	cp "_build/$(OUTFILE)" "$(gamedir)/resourcepacks/$(OUTFILE)"

inplace-build:
	cd data/assets/minecraft/textures/entity/bed && $(PYTHON) make-beds.py
