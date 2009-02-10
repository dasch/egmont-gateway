PYTHON=`which python`
DESTDIR=/
BUILDIR=$(CURDIR)/debian/egmont-gateway
PROJECT=myprojectname
VERSION=0.2

all:
		@echo "make install - Install on local system"
		@echo "make buildrpm - Generate a rpm package"
		@echo "make builddeb - Generate a deb package"
		@echo "make clean - Get rid of scratch and byte files"

install:
		$(PYTHON) setup.py install --root $(DESTDIR) $(COMPILE)

buildrpm:
		$(PYTHON) setup.py bdist_rpm --post-install=rpm/postinstall --pre-uninstall=rpm/preuninstall

builddeb:
		mkdir -p ${BUILDIR}
		DESTDIR=$(BUILDIR) dpkg-buildpackage -rfakeroot

clean:
		$(PYTHON) setup.py clean
		$(MAKE) -f $(CURDIR)/debian/rules clean
		rm -rf build/ MANIFEST
		find . -name '*.pyc' -delete
