import socket
import concurrent.futures
import time
import csv
from datetime import datetime

def port_scan(target, start_port, end_port, timeout=1, fast_scan=False):
    print(f'Starting port scan on {target}...')
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for port in range(start_port, end_port + 1):
            futures.append(executor.submit(scan_port, target, port, timeout))
        for future in concurrent.futures.as_completed(futures):
            port, result = future.result()
            if result:
                open_ports.append(port)
                print(f'Port {port} is open')
    return open_ports

def scan_port(target, port, timeout):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((target, port))
        if result == 0:
            return port, True
        else:
            return port, False
    except Exception as e:
        return port, False
    finally:
        sock.close()

def save_scan_results(filename, target, open_ports):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        for port in open_ports:
            writer.writerow([timestamp, target, port])

if __name__ == "__main__":
    target_host = input("Enter the target IP address or domain name: ")
    start_port = int(input("Enter the starting port number: "))
    end_port = int(input("Enter the ending port number: "))
    fast_scan = input("Do you want to perform a fast scan? (y/n): ").lower() == 'y'

    if fast_scan:
        timeout = 0.5  # Adjust timeout for faster scan
    else:
        timeout = 1

    start_time = time.time()
    open_ports = port_scan(target_host, start_port, end_port, timeout, fast_scan)
    end_time = time.time()
    print("Open ports:", open_ports)
    print("Scan duration:", end_time - start_time, "seconds")

    save_results = input("Do you want to save scan results? (y/n): ").lower() == 'y'
    if save_results:
        filename = input("Enter the filename to save results: ")
        save_scan_results(filename, target_host, open_ports)
        print("Scan results saved to", filename)
