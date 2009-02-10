
import paramiko
import socket

class AuthenticationException(Exception):
    pass

class NetworkError(Exception):
    pass

class AccountClosedException(Exception):
    pass

class Agent:

    def __init__(self, host, port=22):
        self.host = host
        self.port = port
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self, username, password):
        client = self.client
        try:
            client.connect(self.host, self.port, username, password, look_for_keys=False)
            channel = client.invoke_shell()
            channel.recv(1024)
            response = channel.recv(1024)

            if response == "This machine or user is closed.":
                raise AccountClosedException()
        except paramiko.AuthenticationException:
            raise AuthenticationException()
        except socket.error:
            raise NetworkError()
        finally:
            channel.close()
            client.close()
