
import sys
import os
import gtk
import gtk.glade
import pynotify

import gateway
import config
from gateway import AuthenticationException, NetworkError, AccountClosedException
from dialog import display_error


pynotify.init("Egmont Gateway")


def notify(message):
    n = pynotify.Notification("Egmont Gateway", message, "notification-network-ethernet-connected")
    n.set_urgency(pynotify.URGENCY_LOW)
    n.show()


def connect(host, port, username, password):
    try:
        gateway.connect(host, port, username, password)
        notify("You are now connected")
        return True
    except (AuthenticationException, NetworkError, AccountClosedException) as error:
        if type(error) == AuthenticationException: 
            title = "Failed to authenticate"
            message = "Please specify a correct username and password."
        elif type(error) == NetworkError:
            title = "Could not connect to %s on port %i" % (host, port)
            message = "Please make sure you have a network connection."
        elif type(error) == AccountClosedException:
            title = "Your account has been closed"
            message = "You cannot connect to the network until your quota usage drops."
        else:
            title = "Unknown error"
            message = str(error)

        display_error(title, message)

        return False

class Window:

    def __init__(self):
        self.host = config.get_host()
        self.port = config.get_port()
        self.username = config.get_username()
        self.password = config.get_password(self.host, self.port, self.username)
        self.remember = True

        if all((self.host, self.port, self.username, self.password)):
            if connect(self.host, self.port, self.username, self.password):
                sys.exit()

        self.construct()

        if self.host is not None:
            self.host_entry.set_text(self.host)

        if self.port is not None:
            self.port_entry.set_text(str(self.port))

        if self.username is not None:
            self.username_entry.set_text(self.username)

        if self.password is not None:
            self.password_entry.set_text(self.password)

        self.remember_checkbox.set_active(self.remember)
        
    def connect(self, *args):
        self.window.set_sensitive(False)

        if connect(self.host, self.port, self.username, self.password):
            if self.remember:
                password = self.password
            else:
                password = ""

            config.set_credentials(self.host, self.port, self.username, password)
            gtk.main_quit()

        self.window.set_sensitive(True)

    def construct(self):
        dic = {'on_gateway_window_destroy': gtk.main_quit,
               'on_cancel_button_clicked': gtk.main_quit,
               'on_connect_button_clicked': self.connect,
               'on_username_entry_changed': self.username_changed_cb,
               'on_password_entry_changed': self.password_changed_cb,
               'on_host_entry_changed': self.host_changed_cb,
               'on_port_entry_changed': self.port_changed_cb,
               'on_remember_toggled': self.remember_toggled_cb}
        gui = gtk.glade.XML(sys.prefix + "/share/egmont-gateway/glade/egmont.glade")
        gui.signal_autoconnect(dic)

        self.window = gui.get_widget("gateway-window")

        self.host_entry = gui.get_widget("host-entry")
        self.port_entry = gui.get_widget("port-entry")
        self.username_entry = gui.get_widget("username-entry")
        self.password_entry = gui.get_widget("password-entry")
        self.connect_button = gui.get_widget("connect-button")
        self.remember_checkbox = gui.get_widget("remember-checkbox")

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

    def remember_toggled_cb(self, *args):
        self.remember = self.remember_checkbox.get_active()

    def credentials_changed_cb(self):
        self.connect_button.set_sensitive(self.username != "" and self.password != "")
