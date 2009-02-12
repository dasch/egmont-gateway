
import paramiko
import socket


TIMEOUT=10


class AuthenticationException(Exception):
    pass


class NetworkError(Exception):
    pass


class AccountClosedException(Exception):
    pass


def connect(host, port, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(host, port, username, password, look_for_keys=False, timeout=TIMEOUT)
        try:
            channel = client.invoke_shell()
            channel.recv(1024)
            response = channel.recv(1024)

            if response == "This machine or user is closed.":
                raise AccountClosedException()
        finally:
            channel.close()
    except paramiko.AuthenticationException:
        raise AuthenticationException()
    except socket.error:
        raise NetworkError()
    finally:
        client.close()
