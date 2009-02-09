#!/usr/bin/env python

import sys
import os
import gtk
import gtk.glade
import pynotify
import gconf

import gateway

from config import HOST, PORT

class EgmontGateway:

    def __init__(self):
        pynotify.init("Egmont Gateway")

        self.agent = gateway.Agent(host=HOST, port=PORT)
        self.construct()

        client = gconf.client_get_default()

        username = client.get_string('/apps/egmont-gateway/username')
        if username is not None:
            self.username_entry.set_text(username)

        password = client.get_string('/apps/egmont-gateway/password')
        if password is not None:
            self.password_entry.set_text(password)

    def connect(self, *args):
        username = self.username_entry.get_text()
        password = self.password_entry.get_text()

        client = gconf.client_get_default()

        client.set_string('/apps/egmont-gateway/username', username)
        client.set_string('/apps/egmont-gateway/password', password)

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
        except AccountClosedException:
            dialog = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE)
            dialog.set_markup("<b>Your account has been closed</b>")
            dialog.format_secondary_markup("You cannot connect to the network until your quota usage drops.")
            dialog.connect("response", lambda *a: dialog.destroy())
            dialog.run()

    def construct(self):
        pathname = os.path.dirname(sys.argv[0])
        dic = {'on_gateway_window_destroy': gtk.main_quit,
               'on_cancel_button_clicked': gtk.main_quit,
               'on_connect_button_clicked': self.connect,
               'on_username_entry_changed': self.changed_cb,
               'on_password_entry_changed': self.changed_cb}
        window = gtk.glade.XML(pathname + "/egmont.glade")
        window.signal_autoconnect(dic)

        self.username_entry = window.get_widget("username-entry")
        self.password_entry = window.get_widget("password-entry")
        self.connect_button = window.get_widget("connect-button")

    def changed_cb(self, *args):
        username = self.username_entry.get_text()
        password = self.password_entry.get_text()

        self.connect_button.set_sensitive(username != "" and password != "")
    

if __name__ == "__main__":
    eg = EgmontGateway()
    gtk.main()
    sys.exit(0)
