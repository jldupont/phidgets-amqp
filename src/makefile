#
# @author Jean-Lou Dupont
#
#
PRJ=phidgets-dbus

PYTHON=`which python`
BASE=/usr/lib/phidgets-dbus

all:
	@echo "make install"
	@echo "make clean"
	@echo "make buildsrc"

clean:
	@rm -f -r $(DESTDIR)$(BASE)/phidgetsdbus/*.pyc
		
install:
	@install -d $(DESTDIR)$(BASE)
	@install -d $(DESTDIR)$(BASE)/phidgetsdbus
	@install -d $(DESTDIR)$(BASE)/phidgetsdbus/api
	@install -d $(DESTDIR)$(BASE)/phidgetsdbus/apps
	@install -d $(DESTDIR)$(BASE)/phidgetsdbus/phidget
	@install -d $(DESTDIR)$(BASE)/phidgetsdbus/system
	
	@install -d $(DESTDIR)/usr/share/applications
	@install -d $(DESTDIR)/usr/share/icons
	@install -d $(DESTDIR)/usr/bin
	@install -d $(DESTDIR)/usr/lib
	
	@install -D $(CURDIR)/phidgetsdbus/*.py                $(DESTDIR)$(BASE)/phidgetsdbus/
	@install -D $(CURDIR)/phidgetsdbus/api/*.py            $(DESTDIR)$(BASE)/phidgetsdbus/api
	@install -D $(CURDIR)/phidgetsdbus/apps/*.py           $(DESTDIR)$(BASE)/phidgetsdbus/apps
	@install -D $(CURDIR)/phidgetsdbus/phidget/*.py        $(DESTDIR)$(BASE)/phidgetsdbus/phidget
	@install -D $(CURDIR)/phidgetsdbus/system/*.py         $(DESTDIR)$(BASE)/phidgetsdbus/system
	
	@install -D $(CURDIR)/*.py                             $(DESTDIR)$(BASE)/
	@install -D $(CURDIR)/*.desktop                        $(DESTDIR)/usr/share/applications/
	@install -D $(CURDIR)/phidgetsdbus/apps/*.png          $(DESTDIR)/usr/share/icons/ 

	@install $(CURDIR)/phidgets-manager                    $(DESTDIR)/usr/bin/
	@install $(CURDIR)/phidgets-ifk                        $(DESTDIR)/usr/bin/
	@install $(CURDIR)/phidgets-sensors                    $(DESTDIR)/usr/bin/

	@python -m compileall ${DESTDIR}$(BASE)/
	@python -m compileall ${DESTDIR}$(BASE)/phidgetsdbus
	
buildsrc:
	debuild -S