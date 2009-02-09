#!/usr/bin/env python

import sys
import gtk
import gtk.glade
import pynotify

import gateway

from config import HOST, PORT

class EgmontGateway:

    def __init__(self):
        pynotify.init("Egmont Gateway")

        self.agent = gateway.Agent(host=HOST, port=PORT)
        self.construct()

    def connect(self, *args):
        username = self.username_entry.get_text()
        password = self.password_entry.get_text()

        print "Attempting to log in as %s" % username

        try:
            self.agent.connect(username, password)
            n = pynotify.Notification("Egmont Connect",
                                      "You are now connected to the Egmont network.")
            n.show()
            gtk.main_quit()
        except gateway.AuthenticationException:
            dialog = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE)
            dialog.set_markup("<b>Failed to authenticate</b>")
            dialog.format_secondary_markup("Please specify a correct username and password.")
            dialog.connect("response", lambda *a: dialog.destroy())
            dialog.run()
        except gateway.NetworkError:
            dialog = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE)
            dialog.set_markup("<b>Could not connect to network</b>")
            dialog.format_secondary_markup("Please make sure you have a network connection.")
            dialog.connect("response", lambda *a: dialog.destroy())
            dialog.run()

    def construct(self):
        dic = {'on_gateway_window_destroy': gtk.main_quit,
               'on_cancel_button_clicked': gtk.main_quit,
               'on_connect_button_clicked': self.connect}
        window = gtk.glade.XML("egmont.glade")
        window.signal_autoconnect(dic)

        self.username_entry = window.get_widget("username-entry")
        self.password_entry = window.get_widget("password-entry")


if __name__ == "__main__":
    eg = EgmontGateway()
    gtk.main()
    sys.exit(0)
