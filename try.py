import socket
import subprocess
import threading
from datetime import datetime

TARGET_SUBNET = "192.168.1"   # change to match your network
COMMON_PORTS = [21, 22, 23, 80, 135, 139, 443, 445, 3389, 8080]
LIVE_HOSTS = []
lock = threading.Lock()

# ── PING SWEEP ─────────────────────────────────────
def ping_host(ip):
    result = subprocess.run(
        ["ping", "-n", "1", "-w", "300", ip],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    if result.returncode == 0:
        with lock:
            LIVE_HOSTS.append(ip)
            print(f"  [UP]  {ip}")

def ping_sweep(subnet):
    print(f"\n[*] Sweeping {subnet}.0/24 ...\n")
    threads = []
    for i in range(1, 255):
        ip = f"{subnet}.{i}"
        t = threading.Thread(target=ping_host, args=(ip,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print(f"\n[+] {len(LIVE_HOSTS)} host(s) alive\n")

# ── PORT SCAN ──────────────────────────────────────
def scan_port(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        if s.connect_ex((ip, port)) == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "unknown"
            print(f"  [OPEN] {ip}:{port}  ({service})")
        s.close()
    except:
        pass

def port_scan(host):
    print(f"\n[*] Scanning {host} ...\n")
    threads = []
    for port in COMMON_PORTS:
        t = threading.Thread(target=scan_port, args=(host, port))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

# ── MENU ───────────────────────────────────────────
def main():
    print("=" * 38)
    print("       NetScan — Network Tool")
    print("=" * 38)
    print("1. Ping Sweep")
    print("2. Port Scan a host")
    print("3. Both")
    print("4. Exit\n")

    choice = input("Choose [1-4]: ").strip()

    if choice == "1":
        subnet = input("Subnet (e.g. 192.168.1): ").strip()
        ping_sweep(subnet)
    elif choice == "2":
        host = input("Target IP: ").strip()
        port_scan(host)
    elif choice == "3":
        subnet = input("Subnet (e.g. 192.168.1): ").strip()
        ping_sweep(subnet)
        if LIVE_HOSTS:
            for host in LIVE_HOSTS:
                port_scan(host)
        else:
            print("No live hosts to scan.")
    elif choice == "4":
        print("Bye.")
    else:
        print("Invalid choice.")

    print(f"\n[Done] {datetime.now().strftime('%H:%M:%S')}")

main()