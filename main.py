
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
        self.set_border_width(12)

        table = gtk.Table(rows=4, columns=3)
        table.set_col_spacing(0, 12)
        table.set_col_spacing(1, 12)
        table.set_row_spacings(4)
        self.add(table)

        heading = gtk.Label()
        heading.set_markup("<b>Connect to the Egmont Network</b>")
        heading.set_alignment(0, 0.5)
        table.attach(heading, 0, 3, 0, 1)

        username_entry = gtk.Entry()
        username_label = gtk.Label("_Username:")
        username_label.set_use_underline(True)
        username_label.set_mnemonic_widget(username_entry)
        table.attach(username_entry, 2, 3, 2, 3)
        table.attach(username_label, 1, 2, 2, 3)

        password_entry = gtk.Entry()
        password_label = gtk.Label("_Password:")
        password_label.set_use_underline(True)
        password_label.set_mnemonic_widget(password_entry)
        table.attach(password_entry, 2, 3, 3, 4)
        table.attach(password_label, 1, 2, 3, 4)

        table.show_all()


if __name__ == "__main__":
    win = GatewayWindow()
    win.show()

    gtk.main()
