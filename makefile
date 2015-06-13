BINS        = $(wildcard bin/*)
BINS_GLOBAL = $(patsubst bin/%,  /bin/%, $(BINS))
BINS_LOCAL  = $(patsubst bin/%, ~/bin/%, $(BINS))

HOME = $(shell echo $$HOME)

install:   perms $(BINS_GLOBAL)
uninstall: BINS_TARGET = $(BINS_GLOBAL)
uninstall: perms uninstall-to

install-local:   $(BINS_LOCAL)
uninstall-local: BINS_TARGET = $(BINS_LOCAL)
uninstall-local: uninstall-to


uninstall-to:
	@touch $(BINS_TARGET)
	@for file in $(BINS_TARGET) ; do\
		echo REMOVE $$file; \
		rm $$file ;\
	done

/bin/%: bin/%
	@echo INSTALL $@
	@cp $< $@
	@chmod +x $@

$(HOME)/bin/%: bin/%
	@echo INSTALL $@
	@cp $< $@
	@chmod +x $@

	
perms: PERMS = $(shell id -u | grep "^0$$")
perms:
	$(if $(PERMS), $(shell true) ,$(error Need root permissions))

