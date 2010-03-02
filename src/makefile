#
# @author Jean-Lou Dupont
#
#
PRJ=phidgets-amqp

PYTHON=`which python`
BASE=/usr/lib/phidgets-amqp

all:
	@echo "make install"
	@echo "make clean"
	@echo "make buildsrc"

clean:
	@rm -f -r $(DESTDIR)$(BASE)/phidgetsdbus/*.pyc
		
install:
	@install -d $(DESTDIR)$(BASE)
	@install -d $(DESTDIR)$(BASE)/phidgetsamqp
	@install -d $(DESTDIR)$(BASE)/phidgetsamqp/api
	@install -d $(DESTDIR)$(BASE)/phidgetsamqp/apps
	@install -d $(DESTDIR)$(BASE)/phidgetsamqp/phidget
	@install -d $(DESTDIR)$(BASE)/phidgetsamqp/system
	
	@install -d $(DESTDIR)/usr/share/applications
	@install -d $(DESTDIR)/usr/share/icons
	@install -d $(DESTDIR)/usr/bin
	@install -d $(DESTDIR)/usr/lib
	
	@install -D $(CURDIR)/phidgetsamqp/*.py                $(DESTDIR)$(BASE)/phidgetsamqp/
	@install -D $(CURDIR)/phidgetsamqp/api/*.py            $(DESTDIR)$(BASE)/phidgetsamqp/api
	@install -D $(CURDIR)/phidgetsamqp/apps/*.py           $(DESTDIR)$(BASE)/phidgetsamqp/apps
	@install -D $(CURDIR)/phidgetsamqp/phidget/*.py        $(DESTDIR)$(BASE)/phidgetsamqp/phidget
	@install -D $(CURDIR)/phidgetsamqp/system/*.py         $(DESTDIR)$(BASE)/phidgetsamqp/system
	
	@install -D $(CURDIR)/*.py                             $(DESTDIR)$(BASE)/
	@install -D $(CURDIR)/*.desktop                        $(DESTDIR)/usr/share/applications/
	@install -D $(CURDIR)/phidgetsamqp/apps/*.png          $(DESTDIR)/usr/share/icons/ 

	@install $(CURDIR)/phidgets-amqp-manager               $(DESTDIR)/usr/bin/
	@install $(CURDIR)/phidgets-amqp-ifk                   $(DESTDIR)/usr/bin/
	@install $(CURDIR)/phidgets-amqp-sensors               $(DESTDIR)/usr/bin/

	@python -m compileall ${DESTDIR}$(BASE)/
	@python -m compileall ${DESTDIR}$(BASE)/phidgetsdbus
	
buildsrc:
	debuild -S