import paramiko
import socket
import local
import llm
import threading


class HoneypotServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event() 

    def check_auth_password(self, username, password):
        print(f"Login attempt with username: {username} and password: {password}")
        return paramiko.AUTH_SUCCESSFUL

    def get_allowed_auths(self, username):
        return 'password'

    def start(self):
        self.event = paramiko.Event()
        self.event.set()
        return paramiko.OPEN_SUCCEEDED

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

def handle_client(client_socket):
    transport = paramiko.Transport(client_socket)
    transport.add_server_key(paramiko.RSAKey.generate(2048))
    server = HoneypotServer()
    
    try:
        transport.start_server(server=server)
    except paramiko.SSHException:
        print("[!] SSH negotiation failed.")
        return

    channel = transport.accept(20)
    if channel is None:
        print("[!] No channel.")
        return

    print("[+] Authenticated!")
    
    logs = open("history.txt", "a+")
    init = llm.initialize_llm()
    
    try:
        while True:
            channel.send(init)
            message = channel.recv(1024).decode('utf-8').strip()
            logs.write(init + message + "\n")
            words = message.split()
            data = words[0]
            actions = {
                "curl": lambda: local.local_real_time_main(message),
                "wget": lambda: local.local_real_time_main(f"{message} --progress=dot:mega"),
                "mkdir": lambda: local.local(message),
                "touch": lambda: local.local(message),
            }

            if data not in actions:
                init, lines = llm.llm(message)
                logs.write(lines)
                channel.send(lines)
            else:
                output = actions.get(data)()
                channel.send(init + output)
                logs.write(output + "\n")
                llm.add_chat(message, output)
    except Exception as e:
        print(f"[!] Exception: {str(e)}")
    finally:
        channel.close()

def start_honeypot(host='0.0.0.0', port=2222):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(100)

    print(f"[*] Listening for connections on {host}:{port} ...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[*] Connection from {addr}")
        handle_client(client_socket)

if __name__ == "__main__":
    start_honeypot()
