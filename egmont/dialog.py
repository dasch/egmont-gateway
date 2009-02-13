
import gtk

def display_error(title, message):
    dialog = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE)
    dialog.set_markup("<b>%s</b>" % title)
    dialog.format_secondary_markup(message)
    dialog.connect("response", lambda *a: dialog.destroy())
    dialog.run()
