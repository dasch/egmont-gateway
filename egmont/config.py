
import gnomekeyring as gkeyring
import gconf

try:
    KEYRING = gkeyring.get_default_keyring_sync()
except gkeyring.NoKeyringDaemonError:
    KEYRING = None

GCONF_CLIENT = gconf.client_get_default()


DEFAULT_HOST = "bifrost.egmont-kol.dk"
DEFAULT_PORT = 22


_get_password = gkeyring.find_network_password_sync
_set_password = gkeyring.set_network_password_sync


def _get_string(key):
    return GCONF_CLIENT.get_string('/apps/egmont-gateway/%s' % key)

def _set_string(key, value):
    GCONF_CLIENT.set_string('/apps/egmont-gateway/%s' % key, value)


def get_password(host, port, username):
    if KEYRING is None:
        return

    try:
        items = _get_password(server=host, port=port, protocol="ssh", user=username)

        if len(items) is not 0:
            return items[0]["password"]
    except gkeyring.NoMatchError:
        pass


def set_credentials(host, port, username, password):
    set_host(host)
    set_port(port)
    set_username(username)

    if KEYRING is not None:
        _set_password(user=username, password=password,
                      server=host, port=port, protocol="ssh")


def get_username():
    return _get_string('username')


def set_username(username):
    _set_string('username', username)


def get_host():
    return _get_string('host') or DEFAULT_HOST


def set_host(host):
    _set_string('host', host)


def get_port():
    return GCONF_CLIENT.get_int('/apps/egmont-gateway/port') or DEFAULT_PORT


def set_port(port):
    return GCONF_CLIENT.set_int('/apps/egmont-gateway/port', port)
