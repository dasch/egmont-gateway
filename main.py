
import gtk
import gateway

from config import HOST, PORT

class GatewayWindow(gtk.Window):

    def __init__(self):
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)

        self.set_title("Egmont Gateway")

        self.agent = gateway.Agent(host=HOST, port=PORT)

        self.construct()

    def connect(self):
        self.agent.connect(self.username, self.password)

    def construct(self):
        vbox = gtk.VBox()

        table = gtk.Table(rows=3, columns=2)
        self.add(table)

        username_entry = gtk.Entry()
        username_label = gtk.Label("_Username:")
        username_label.set_use_underline(True)
        username_label.set_mnemonic_widget(username_entry)
        table.attach(username_entry, 1, 2, 0, 1)
        table.attach(username_label, 0, 1, 0, 1)

        password_entry = gtk.Entry()
        password_label = gtk.Label("_Password:")
        password_label.set_use_underline(True)
        password_label.set_mnemonic_widget(password_entry)
        table.attach(password_entry, 1, 2, 1, 2)
        table.attach(password_label, 0, 1, 1, 2)

        table.show_all()


if __name__ == "__main__":
    win = GatewayWindow()
    win.show()

    gtk.main()
