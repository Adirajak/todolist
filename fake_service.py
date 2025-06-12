import socket
import threading
import datetime
from honeypot.logger import log_attack

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 2222       # Common non-standard SSH port for honeypot

def handle_client(conn, addr):
    ip = addr[0]
    print(f"[+] Connection attempt from {ip}")

    # Log connection attempt with timestamp
    log_attack(ip, "Connection Attempt", datetime.datetime.now())

    try:
        conn.sendall(b"SSH-2.0-OpenSSH_7.4p1 FakeSSH\r\n")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            command = data.decode(errors='ignore').strip()
            print(f"[{ip}] Command: {command}")

            # Log the received command
            log_attack(ip, f"Command: {command}", datetime.datetime.now())

            # Send fake response
            conn.sendall(b"bash: command not found\r\n")
    except Exception as e:
        print(f"Error handling client {ip}: {e}")
    finally:
        conn.close()
        print(f"[-] Connection closed for {ip}")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[*] Fake SSH honeypot listening on port {PORT}")

    while True:
        conn, addr = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

if __name__ == "__main__":
    start_server()


# Add import
from alerts import send_email_alert

# Example usage inside handle_client, after logging the attack:
# (Make sure this is inside the handle_client function and after 'ip', 'command', and 'attempt' are defined)
# log_attack(ip, attempt, command)

# Send alert email
# subject = f"Honeypot Alert: Attack attempt from {ip}"
# message = f"Time: {datetime.datetime.now()}\nIP: {ip}\nCommand: {command}\nAttempt Type: {attempt}"
# send_email_alert(subject, message)
