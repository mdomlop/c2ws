NAME='c2ws'
PREFIX='/usr'
TEMPDIR := $(shell mktemp -u --suffix .$(NAME))

install:
	install -Dm 755 src/$(NAME).py $(PREFIX)/bin/$(NAME)
	install -Dm 644 LICENSE $(PREFIX)/share/licenses/$(NAME)/COPYING
	install -Dm 644 README.md $(PREFIX)/share/doc/$(NAME)/README

uninstall:
	rm -f $(PREFIX)/bin/$(NAME)

clean:
	rm -f packages/pacman/$(NAME)-*.pkg.tar.xz

togit: clean
	git add .
	git commit -m "Updated from makefile"
	git push origin

pacman:
	mkdir $(TEMPDIR)
	cp packages/pacman/PKGBUILD $(TEMPDIR)/
	cd $(TEMPDIR); makepkg -dr
	cp $(TEMPDIR)/$(NAME)-*.pkg.tar.xz packages/pacman/
	rm -rf $(TEMPDIR)
	@echo Package done!
	@echo Package is in `pwd`/packages/pacman/
