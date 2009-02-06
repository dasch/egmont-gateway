
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

        username_label = gtk.Label("Username")
        table.attach(username_label, 0, 1, 0, 1)

        username_entry = gtk.Entry()
        table.attach(username_entry, 1, 2, 0, 1)

        table.show_all()


if __name__ == "__main__":
    win = GatewayWindow()
    win.show()

    gtk.main()
