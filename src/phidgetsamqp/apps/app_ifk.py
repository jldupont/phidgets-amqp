"""
    @author: jldupont

    Created on 2010-02-23
"""
__all__=[]
import os
import gtk #@UnresolvedImport

from system.mbus import Bus

class AppPopupMenu:
    def __init__(self, app):
        self.item_exit = gtk.MenuItem( "exit", True)
        self.item_exit.connect( 'activate', app.exit)

        self.menu = gtk.Menu()
        self.menu.append( self.item_exit)
        self.menu.show_all()

    def show_menu(self, button, time):
        self.menu.popup( None, None, None, button, time)
        

class AppIcon(object):
    
    ICON_PATH="/usr/share/icons/"
    ICON_FILE="phidgets-amqp-ifk.png"
    
    def __init__(self):
        self.curdir=os.path.abspath( os.path.dirname(__file__) )
    
    def getIconPixBuf(self): 
        try:
            ipath=self.ICON_PATH+"/"+self.ICON_FILE
            pixbuf = gtk.gdk.pixbuf_new_from_file( ipath )
        except:
            ipath=self.curdir+"/"+self.ICON_FILE
            pixbuf = gtk.gdk.pixbuf_new_from_file( ipath )
                      
        return pixbuf.scale_simple(24,24,gtk.gdk.INTERP_BILINEAR)
        

class App(object):
    def __init__(self):
        
        self.popup_menu=AppPopupMenu(self)
        
        self.tray=gtk.StatusIcon()
        self.tray.set_visible(True)
        self.tray.set_tooltip("Phidgets-AMQP, InterfaceKit")
        self.tray.connect('popup-menu', self.do_popup_menu)
        
        scaled_buf = AppIcon().getIconPixBuf()
        self.tray.set_from_pixbuf( scaled_buf )
        
    def do_popup_menu(self, status, button, time):
        self.popup_menu.show_menu(button, time)

    def exit(self, *p):
        Bus.publish("App", "%quit")


_app=App()
