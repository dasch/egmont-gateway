
import sys
import os
import gtk
import gtk.glade
import pynotify

import gateway
import config

class Window:

    def __init__(self):
        pynotify.init("Egmont Gateway")

        self.construct()

        self.host = config.get_host()
        self.port = config.get_port()
        self.username = config.get_username()
        self.password = config.get_password(self.host, self.port, self.username)

        if self.host is not None:
            self.host_entry.set_text(self.host)

        if self.port is not None:
            self.port_entry.set_text(str(self.port))

        if self.username is not None:
            self.username_entry.set_text(self.username)

        if self.password is not None:
            self.password_entry.set_text(self.password)
        
    def connect(self, *args):
        config.set_credentials(self.host, self.port, self.username, self.password)

        try:
            gateway.connect(self.host, self.port, self.username, self.password)
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
        except gateway.AccountClosedException:
            dialog = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE)
            dialog.set_markup("<b>Your account has been closed</b>")
            dialog.format_secondary_markup("You cannot connect to the network until your quota usage drops.")
            dialog.connect("response", lambda *a: dialog.destroy())
            dialog.run()

    def construct(self):
        dic = {'on_gateway_window_destroy': gtk.main_quit,
               'on_cancel_button_clicked': gtk.main_quit,
               'on_connect_button_clicked': self.connect,
               'on_username_entry_changed': self.username_changed_cb,
               'on_password_entry_changed': self.password_changed_cb,
               'on_host_entry_changed': self.host_changed_cb,
               'on_port_entry_changed': self.port_changed_cb}
        window = gtk.glade.XML(sys.prefix + "/share/egmont-gateway/glade/egmont.glade")
        window.signal_autoconnect(dic)

        self.host_entry = window.get_widget("host-entry")
        self.port_entry = window.get_widget("port-entry")
        self.username_entry = window.get_widget("username-entry")
        self.password_entry = window.get_widget("password-entry")
        self.connect_button = window.get_widget("connect-button")

    def host_changed_cb(self, *args):
        self.host = self.host_entry.get_text()

    def port_changed_cb(self, *args):
        self.port = int(self.port_entry.get_text())

    def username_changed_cb(self, *args):
        self.username = self.username_entry.get_text()
        self.credentials_changed_cb()

    def password_changed_cb(self, *args):
        self.password = self.password_entry.get_text()
        self.credentials_changed_cb()

    def credentials_changed_cb(self):
        self.connect_button.set_sensitive(self.username != "" and self.password != "")
