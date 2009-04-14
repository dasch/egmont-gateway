
import paramiko
import socket


TIMEOUT=10


class AuthenticationException(Exception):
    """Raised when invalid credentials are given."""
    pass


class NetworkError(Exception):
    """Raised when network errors occur."""
    pass


class AccountClosedException(Exception):
    """Raised if the account has been closed."""
    pass


def connect(host, port, username, password):
    """Connect to the given host."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        options = {"look_for_keys": False, "allow_agent": False, "timeout": TIMEOUT}
        client.connect(host, port, username, password, **options)
        try:
            channel = client.invoke_shell()

            while True:
                response = channel.recv(1024)

                if response == "":
                    break
                elif "machine or user is closed" in response:
                    raise AccountClosedException()
        finally:
            channel.close()
    except paramiko.AuthenticationException:
        raise AuthenticationException()
    except socket.error:
        raise NetworkError()
    finally:
        client.close()
