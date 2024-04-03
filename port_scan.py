import socket

def port_scan(target, start_port, end_port):
    print(f'Starting port scan on {target}...')
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f'Port {port} is open')
        sock.close()

if __name__ == "__main__":
    target_host = input("Enter the target IP address or domain name: ")
    start_port = int(input("Enter the starting port number: "))
    end_port = int(input("Enter the ending port number: "))

    port_scan(target_host, start_port, end_port)
