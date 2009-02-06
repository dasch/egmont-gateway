
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
            dialog = gtk.Dialog("Invalid username or password")
            dialog.add(gtk.Label("Please specify another username or password."))
            dialog.add_button(gtk.STOCK_OK, 0)
            dialog.connect("response", lambda *a: dialog.destroy())
            dialog.show()

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
