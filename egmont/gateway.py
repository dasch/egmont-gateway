
import paramiko
import socket

HOST = "bifrost.egmont-kol.dk"
PORT = 22

class AuthenticationException(Exception):
    pass

class NetworkError(Exception):
    pass

class AccountClosedException(Exception):
    pass

class Agent:

    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self, username, password):
        client = self.client
        try:
            client.connect(self.host, self.port, username, password, look_for_keys=False)
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
