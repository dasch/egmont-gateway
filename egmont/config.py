
import gnomekeyring as gkeyring
import gconf

KEYRING = gkeyring.get_default_keyring_sync()
GCONF_CLIENT = gconf.client_get_default()


DEFAULT_HOST = "bifrost.egmont-kol.dk"
DEFAULT_PORT = 22


def get_password(host, port, username):
    try:
        items = gkeyring.find_network_password_sync(server=host,
                                                    port=port,
                                                    protocol="ssh",
                                                    user=username)

        if len(items) is not 0:
            return items[0]["password"]
    except gkeyring.NoMatchError:
        pass


def set_credentials(host, port, username, password):
    set_host(host)
    set_port(port)
    set_username(username)

    gkeyring.set_network_password_sync(user=username,
                                       password=password,
                                       server=host,
                                       port=port,
                                       protocol="ssh")


def get_username():
    return GCONF_CLIENT.get_string('/apps/egmont-gateway/username')


def set_username(username):
    return GCONF_CLIENT.set_string('/apps/egmont-gateway/username', username)


def get_host():
    return GCONF_CLIENT.get_string('/apps/egmont-gateway/host') or DEFAULT_HOST


def set_host(host):
    return GCONF_CLIENT.set_string('/apps/egmont-gateway/host', host)


def get_port():
    return GCONF_CLIENT.get_int('/apps/egmont-gateway/port') or DEFAULT_PORT


def set_port(port):
    return GCONF_CLIENT.set_int('/apps/egmont-gateway/port', port)
